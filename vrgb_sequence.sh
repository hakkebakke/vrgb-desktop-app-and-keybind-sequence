#!/bin/bash

# Sjekk at skriptet kjører som root (siden kommandoene krever det)
if [ "$EUID" -ne 0 ]; then
  echo "Feil: Dette skriptet må kjøres som root (sudo)." >&2
  exit 1
fi

# Fil som holder styr på hvilket trinn vi er på (1-12)
STATE_FILE="/tmp/vrgb_step.txt"

# Les forrige trinn, eller start på 1 hvis filen ikke finnes
if [ -f "$STATE_FILE" ]; then
    STEP=$(cat "$STATE_FILE")
else
    STEP=1
fi

# Kjør riktig kommando basert på hvilket trinn vi er på
case $STEP in
    1)  vrgb set FF0000 100 ;;
    2)  vrgb set FF8000 100 ;;
    3)  vrgb set FFFF00 100 ;;
    4)  vrgb set 80FF00 100 ;;
    5)  vrgb set 00FF00 100 ;;
    6)  vrgb set 00FF80 100 ;;
    7)  vrgb set 00FFFF 100 ;;
    8)  vrgb set 0080FF 100 ;;
    9)  vrgb set 0000FF 100 ;;
    10) vrgb set 7F00FF 100 ;;
    11) vrgb set FF00FF 100 ;;
    12) vrgb set FF007F 100 ;;
esac

# Beregn neste trinn (1-12). Hvis vi bikker 12, start på 1 igjen.
NEXT_STEP=$(( (STEP % 12) + 1 ))

# Lagre det neste trinnet til neste gang du trykker
echo "$NEXT_STEP" > "$STATE_FILE"

