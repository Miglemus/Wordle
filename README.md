# Wordle

## Cython/OpenMP acceleration

The solver can use a Cython extension (`core.solver_accel`) to score guesses in
parallel with OpenMP. The Python fallback still works when the extension is not
available.

On Ubuntu/Debian, install the Python headers before building the extension:

```bash
sudo apt install python3.12-dev
uv sync --reinstall-package wordle
```

You can control OpenMP's thread count with:

```bash
OMP_NUM_THREADS=8 uv run python main.py --solver fast
```

Use the pure Python solver with:

```bash
uv run python main.py --solver classic
```
