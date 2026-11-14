# spiderweb-gateway 🕸️

Ein Sicherheits-Gateway für den AI-Zugang von Bankmitarbeitenden.

**Problem:** Hat ein Angreifer den Laptop eines Mitarbeiters übernommen, kann er dessen
AI-Assistenten missbrauchen, um über angebundene Wissensdatenbanken daten abzuziehen, ohne tiefer ins Netz einzudringen.

**Lösung:** Jeder Mitarbeitende bewegt sich in einem Netz aus Regeln.
Das Gateway prüft jede AI-Anfrage gegen feste Rollengrenzen und das gewohnte Verhalten der Person. Bei einem Verstoss wird der AI-Zugang eingefroren und das SOC-Team alamiert.

## Fahrplan
[X] Fake-LLM für deterministische Tests
[] Gateway als Proxy mit Logging
[] Identität per Token
[] Rollen-Policy und Freeze
[] SOC-Seite
[] Fake-Wissensdatenbank
[] Verhaltens-Baseline pro Person
[] Angriffsszenarien

**Status:** in Entwicklung