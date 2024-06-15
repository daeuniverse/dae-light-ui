# dae-light-ui

## What this project is for

A lightweight dashboard for [dae](https://github.com/daeuniverse/dae)

Project Goals:

- Extremely lightweight and portable
- Easy to use
- Dark mode

Alternatively, please consider adopting [daed](https://github.com/daeuniverse/daed), which offers better experience.

## Status

👷 This project is currently under development.

## Preview

<img width="1658" alt="image" src="https://github.com/daeuniverse/dae-light-ui/assets/31861128/3d616287-7f27-4445-958a-b70bfad052cf">

## Bootstrap

```bash
./install
```

## Install

coming soon.

## Usage

Export envs

```bash
export CONFIG_PATH=/etc/dae/config.dae
export DAE_BIN_PATH=/usr/bin/dae
```

Run locally

```bash
python3 app.py
```

Run as container

```bash
# run
docker compose up -d --force-recreate --build

# inspect logs
docker logs -f dae-light-ui
```

Compile as binary

```bash
./venv/bin/pyinstall app.py
```

## TODOs

- [x] Add theming support
- [ ] Add support to update geodate
- [ ] Fix pid parsing at the container level
