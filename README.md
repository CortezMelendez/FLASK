# FLASK API Project

This project is a small Flask API created as a practical exercise to expose JSON data and basic route logic using `app.py` and the local JSON file `API.json`.

## Project purpose

The application loads data from `API.json` and exposes it through multiple routes. The project is intended as a reference and learning base for building simple REST-style endpoints with Flask.

## Repository status

Current local branch detected in the project:

- `feature`

Remote branches found in the repository:

- `main`
- `feature`
- `hotfix`
- `release`
- `release2`
- `release3`
- `release4`

## Main files

- `app.py` — Flask application with the route definitions.
- `API.json` — source data used by the API routes.
- `req.txt` — Python dependencies.
- `U1/` and `U2/` — practice files and classroom exercises.

## Run the app

1. Open a terminal in the project folder.
2. Activate the virtual environment:
   - macOS/Linux: `source venv/bin/activate`
3. Start the app:
   - `python3 app.py`
4. The app will run with Flask debug mode on:
   - `http://127.0.0.1:5000/`

## Repository branches found

The repository was scanned and the following branches are available in the remote repository:

- `main`
- `feature`
- `hotfix`
- `release`
- `release2`
- `release3`
- `release4`

The current local branch used for this project is:

- `feature`

## Planned API routes (10 GET endpoints)

The original project comments indicate that the next step is to create 10 `GET` endpoints, one for each function, to continue expanding the API.

### 1) Reading and displaying data from the dictionary

These endpoints are meant to show network/device information already stored in `API.json`.

1. `GET /routers`  
   Returns the complete list of routers in the JSON dataset.

2. `GET /router/<mac>`  
   Returns all information for a specific router by MAC address.

3. `GET /router/name/<mac>`  
   Returns only the `name` value for a requested router.

4. `GET /router/protocolos/<mac>`  
   Returns the routing protocols configured for a router.

5. `GET /router/vlans/<mac>`  
   Returns the VLAN information for a particular device.

### 2) Generating or inventing new data

These endpoints are meant to create synthetic responses for future development and tests.

6. `GET /servidor`  
   Returns a generic server object with basic metadata.

7. `GET /servidor_2`  
   Returns a second server example with different host information.

8. `GET /inventario`  
   Returns a mocked inventory of network equipment.

9. `GET /politicas`  
   Returns a policy list for access control or routing rules.

10. `GET /status`  
    Returns workflow or device status information such as online/offline states.

These route definitions are a roadmap for future versions of the app, where the goal is to build 10 GET-type routes in a structured way, updating and managing the data progressively.

## Routes defined in app.py

### 1) Root route

- Method: `GET`
- URL: `/`
- Function: `inicio()`
- Behavior:
  - Returns the value stored in `datos_json["AB::10C::7D::"]`.
  - This is the first data entry loaded from `API.json`.
  - It is used as a basic landing page / HTML-type endpoint.

Example:

- `http://127.0.0.1:5000/`

Response:

```json
{
  "name": "R1",
  "protocolos": ["OSPF,S.T,IGRP"],
  "vlans": {
    "vl1": {
      "Ports": ["G0/0", "G0/1", "G0/2", "G0/3"],
      "policies": ["SSH", "ACL", "VLAN", "STP"],
      "ET": true,
      "IP": "192.168.10.68",
      "SSH": true
    }
  }
}
```

### 2) Dynamic JSON route

- Method: `GET`
- URL: `/json/<mac>`
- Function: `json_data(mac)`
- Behavior:
  - Receives a MAC address-like value from the URL.
  - Looks it up in `API.json` using the dictionary key `mac`.
  - Prints the data from the selected record:
    - `name`
    - `protocolos`
    - `vlans`
    - `status`
  - Returns only the `name` field from the matched entry.

Examples:

- `http://127.0.0.1:5000/json/AA::10C::7D::01`
- `http://127.0.0.1:5000/json/AA::10C::7D::02`
- `http://127.0.0.1:5000/json/AB::10C::7D::`

Example response:

```text
R1
```

If the value does not exist in `API.json`, Flask will return an error because the dictionary key is not found.

### 3) Static JSON endpoint

- Method: `GET`
- URL: `/servidor_1`
- Function: `servidor_1()`
- Behavior:
  - Returns a hardcoded JSON response using Flask `jsonify`.
  - It simulates a server configuration object with network and policy metadata.

Example:

- `http://127.0.0.1:5000/servidor_1`

Response:

```json
{
  "0001": {
    "ip": "192.168.0.1",
    "divice": "Router",
    "policy": ["Ro", "Not Allowed", [0.2, 0.3, 0.5]],
    "status": true
  }
}
```

## Route map

```mermaid
flowchart TD
    A[Client / Browser] --> B[GET /]
    A --> C[GET /json/<mac>]
    A --> D[GET /servidor_1]

    B --> E[inicio()]
    C --> F[json_data(mac)]
    D --> G[servidor_1()]

    E --> H[Reads API.json["AB::10C::7D::"]]
    F --> I[Looks up API.json[mac]]
    G --> J[Returns static JSON payload]
```

## Route summary table

| Route | Method | Function | Description |
|---|---|---|---|
| `/` | `GET` | `inicio()` | Returns the first router record from `API.json` |
| `/json/<mac>` | `GET` | `json_data(mac)` | Reads a router entry by key and returns the `name` |
| `/servidor_1` | `GET` | `servidor_1()` | Returns a synthetic server JSON payload |

## Notes for future development

The file `app.py` includes comments suggesting the next step for the project:

- Create 10 GET-type functions.
- Change the data gradually.
- Generate loops based on dictionary data.
- Build 5 endpoints to display dictionary elements.
- Build 5 endpoints to invent or simulate additional data.

This project is a base template for evolving into a bigger Flask API with additional network-device information.

## Initial version

This README was created as part of the initial project version and documents the current state of the app before further API expansion.
