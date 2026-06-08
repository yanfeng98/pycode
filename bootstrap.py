from __future__ import annotations

import logging_utils as _log

_bootstrapped: bool = False


def bootstrap(config: dict) -> None:
    global _bootstrapped

    _log.configure_from_config(config)
    _log.info("bootstrap_start",
              model=config.get("model", ""),
              version=_get_version(),
              shell_policy=config.get("shell_policy", "allow"),
              allowed_root=config.get("allowed_root") or "(unrestricted)")

    import tools as _tools  # noqa: F401
    _log.debug("bootstrap_tools_ready")

    port = config.get("health_check_port")
    if port:
        try:
            from health import start_health_server
            start_health_server(int(port), config)
            _log.info("health_server_started", port=int(port))
        except Exception as exc:
            _log.warn("health_server_failed", error=str(exc)[:200])

    _bootstrapped = True
    _log.info("bootstrap_done")


def _get_version() -> str:
    try:
        import pycode
        return getattr(pycode, "VERSION", "unknown")
    except Exception:
        return "unknown"
