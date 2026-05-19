# -*- coding: utf-8 -*-
# @Author: LetMeFly
# @Description: Estrategia leechersAndSeeders corregida (V2)

from __future__ import annotations
import math
import logging
from typing import Dict, List, Optional, Tuple

from src.getter.getBYR.BYR import BYR
from src.client.qBittorrent.QBittorrent import QBittorrent
import config.secret as secret

logger = logging.getLogger(__name__)

BOT_CATEGORY: str = "RyukawaChihiro_leechersAndSeeders"

def _calc_score(leechers: int, seeders: int) -> float:
    return leechers / (seeders + 1)

def _gb_to_bytes(gb: float) -> int:
    return int(gb * (1024 ** 3))

def _bytes_to_gb(b: int) -> float:
    return round(b / (1024 ** 3), 2)

class LeechersAndSeedersController:
    def __init__(self, byr: BYR, client: QBittorrent, max_disk_gb: float, min_score: float = 0.5, save_path: Optional[str] = None) -> None:
        self.byr = byr
        self.client = client
        self.max_disk_bytes = _gb_to_bytes(max_disk_gb)
        self.min_score = min_score
        self.save_path = save_path or ""

    def run(self) -> None:
        logger.info("[leechersAndSeeders] ── Ciclo de refresco iniciado ──")
        site_torrents: List[Dict] = self.byr.getAllFreeTorrents()
        if not site_torrents:
            logger.info("[leechersAndSeeders] No hay torrents free en el sitio.")
            return

        for t in site_torrents:
            t["_score"] = _calc_score(t["leechers"], t["seeders"])

        candidates: List[Dict] = sorted(
            [t for t in site_torrents if t["_score"] >= self.min_score],
            key=lambda t: t["_score"],
            reverse=True
        )

        active: List[Dict] = self._get_bot_torrents()
        active_site_ids: set = {t["site_id"] for t in active if t.get("site_id")}
        candidate_score_by_id: Dict[str, float] = {t["id"]: t["_score"] for t in candidates}

        for torrent in candidates:
            tid = torrent["id"]
            if tid in active_site_ids:
                continue

            needed = torrent["size"]
            ok, active = self._ensure_space(needed, active, candidate_score_by_id)
            if not ok:
                continue

            self._download(torrent)
            active = self._get_bot_torrents()
            active_site_ids = {t["site_id"] for t in active if t.get("site_id")}
        logger.info("[leechersAndSeeders] ── Ciclo completado ──")

    def _ensure_space(self, needed_bytes: int, active: List[Dict], candidate_score_by_id: Dict[str, float]) -> Tuple[bool, List[Dict]]:
        used = sum(t.get("size", 0) for t in active)
        free = self.max_disk_bytes - used
        if free >= needed_bytes:
            return True, active

        def eviction_key(at: Dict) -> float:
            sid = at.get("site_id")
            if not sid or sid not in candidate_score_by_id:
                return -math.inf
            return candidate_score_by_id[sid]

        eviction_order = sorted(active, key=eviction_key)
        for victim in eviction_order:
            if free >= needed_bytes:
                break
            size = victim.get("size", 0)
            h = victim["hash"]
            self.client.deleteTorrent(h, deleteFiles=True)
            free += size
            active = [t for t in active if t["hash"] != h]

        return free >= needed_bytes, active

    def _download(self, torrent: Dict) -> None:
        torrent_hash = self.byr.getHashById(torrent["id"])
        if not torrent_hash:
            return
        kwargs = {}
        if self.save_path:
            kwargs["savePath"] = self.save_path
        kwargs["category"] = BOT_CATEGORY
        self.client.addNewTorrent(torrent_hash, **kwargs)

    def _get_bot_torrents(self) -> List[Dict]:
        return self.client.getTorrentList(category=BOT_CATEGORY)
