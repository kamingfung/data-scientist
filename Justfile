# Sync hk-* skills from sibling hk-agent-skills repo (or GitHub if absent)
sync-hk:
    #!/usr/bin/env sh
    set -e
    if [ -d ../hk-agent-skills/skills ]; then
        cp -R ../hk-agent-skills/skills/hk-* skills/
        echo "Synced hk-* skills from ../hk-agent-skills/skills"
    else
        npx --yes skills add kamingfung/hk-agent-skills -y
    fi
