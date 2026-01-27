# MAReK


## Development

Run app:
```bash
uv run python src/main.py
```

Build:
```bash
uv run pyside6-deploy --config-file pysidedeploy.spec
```

```bash
uv run pyinstaller --onedir --windowed --name MAReK src/main.py
```

```bash
makensis installer.nsi
```
