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

### Server dictionary structure

The application defines a `servidores` dictionary in [app.py](app.py). It contains 10 mock devices with the following general structure:

```python
{
  "0001": {
    "ip": "192.168.0.1",
    "device": "Router Principal",
    "policy": ["Ro", "Not Allowed", [0.2, 0.3, 0.5]],
    "status": True
  }
}
```

Each server entry includes:

- `ip`: network address
- `device`: device name or role
- `policy`: access or rule configuration
- `status`: boolean active/inactive state

### Server route descriptions

#### 1) `/servidor_1`

- Method: `GET`
- Function: `servidor_1()`
- Description: returns the first device entry from the server dictionary.
- Data returned:
  - ID: `0001`
  - IP: `192.168.0.1`
  - Device: `Router Principal`
  - Policy: `Ro`, `Not Allowed`, `[0.2, 0.3, 0.5]`
  - Status: `True`

#### 2) `/servidor_2`

- Method: `GET`
- Function: `servidor_2()`
- Description: returns the second device, a switch on the first floor.
- Data returned:
  - ID: `0002`
  - IP: `192.168.0.2`
  - Device: `Switch Piso 1`
  - Policy: `Rw`, `Allowed`
  - Status: `True`

#### 3) `/servidor_3`

- Method: `GET`
- Function: `servidor_3()`
- Description: returns the firewall core device.
- Data returned:
  - ID: `0003`
  - IP: `192.168.0.3`
  - Device: `Firewall Core`
  - Policy: `Block All`
  - Status: `True`

#### 4) `/servidor_4`

- Method: `GET`
- Function: `servidor_4()`
- Description: returns a web server that is currently inactive.
- Data returned:
  - ID: `0004`
  - IP: `192.168.0.4`
  - Device: `Servidor Web`
  - Policy: `HTTP`, `HTTPS`
  - Status: `False`

#### 5) `/servidor_5`

- Method: `GET`
- Function: `servidor_5()`
- Description: returns an access point device.
- Data returned:
  - ID: `0005`
  - IP: `192.168.0.5`
  - Device: `Access Point`
  - Policy: `WPA3`
  - Status: `True`

#### 6) `/servidor_6`

- Method: `GET`
- Function: `servidor_6()`
- Description: creates and returns a new device entry for a network printer.
- Added data:
  - ID: `0006`
  - IP: `192.168.0.6`
  - Device: `Impresora de Red`
  - Policy: `Print Only`
  - Status: `True`

#### 7) `/servidor_7`

- Method: `GET`
- Function: `servidor_7()`
- Description: creates and returns a NAS storage server.
- Added data:
  - ID: `0007`
  - IP: `192.168.0.7`
  - Device: `Servidor NAS Almacenamiento`
  - Policy: `Backup`, `Restricted`
  - Status: `True`

#### 8) `/servidor_8`

- Method: `GET`
- Function: `servidor_8()`
- Description: creates and returns a security IP camera.
- Added data:
  - ID: `0008`
  - IP: `192.168.0.8`
  - Device: `Cámara IP Seguridad`
  - Policy: `Stream Only`
  - Status: `True`

#### 9) `/servidor_9`

- Method: `GET`
- Function: `servidor_9()`
- Description: creates and returns a UPS device used for smart backup monitoring.
- Added data:
  - ID: `0009`
  - IP: `192.168.0.9`
  - Device: `UPS Smart Respaldos`
  - Policy: `Monitor Only`
  - Status: `False`

#### 10) `/servidor_10`

- Method: `GET`
- Function: `servidor_10()`
- Description: creates and returns a telemetry sensor for the data center.
- Added data:
  - ID: `0010`
  - IP: `192.168.0.10`
  - Device: `Sensor Telemetría DataCenter`
  - Policy: `IoT Device`
  - Status: `True`

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
    A --> E[GET /servidor_2]
    A --> F[GET /servidor_3]
    A --> G[GET /servidor_4]
    A --> H[GET /servidor_5]
    A --> I[GET /servidor_6]
    A --> J[GET /servidor_7]
    A --> K[GET /servidor_8]
    A --> L[GET /servidor_9]
    A --> M[GET /servidor_10]

    B --> N[inicio()]
    C --> O[json_data(mac)]
    D --> P[servidor_1()]
    E --> Q[servidor_2()]
    F --> R[servidor_3()]
    G --> S[servidor_4()]
    H --> T[servidor_5()]
    I --> U[servidor_6()]
    J --> V[servidor_7()]
    K --> W[servidor_8()]
    L --> X[servidor_9()]
    M --> Y[servidor_10()]

    N --> Z[Loads data from API.json]
    O --> AA[Looks up device by MAC]
    P --> AB[Returns 0001]
    Q --> AC[Returns 0002]
    R --> AD[Returns 0003]
    S --> AE[Returns 0004]
    T --> AF[Returns 0005]
    U --> AG[Adds 0006]
    V --> AH[Adds 0007]
    W --> AI[Adds 0008]
    X --> AJ[Adds 0009]
    Y --> AK[Adds 0010]
```

## Route summary table

| Route | Method | Function | Description |
|---|---|---|---|
| `/` | `GET` | `inicio()` | Returns the first router record from `API.json` |
| `/json/<mac>` | `GET` | `json_data(mac)` | Reads a router entry by key and returns the `name` |
| `/servidor_1` | `GET` | `servidor_1()` | Returns the main router device `0001` |
| `/servidor_2` | `GET` | `servidor_2()` | Returns the first-floor switch `0002` |
| `/servidor_3` | `GET` | `servidor_3()` | Returns the firewall core `0003` |
| `/servidor_4` | `GET` | `servidor_4()` | Returns the web server `0004` |
| `/servidor_5` | `GET` | `servidor_5()` | Returns the access point `0005` |
| `/servidor_6` | `GET` | `servidor_6()` | Adds and returns the network printer `0006` |
| `/servidor_7` | `GET` | `servidor_7()` | Adds and returns the NAS server `0007` |
| `/servidor_8` | `GET` | `servidor_8()` | Adds and returns the security IP camera `0008` |
| `/servidor_9` | `GET` | `servidor_9()` | Adds and returns the UPS backup device `0009` |
| `/servidor_10` | `GET` | `servidor_10()` | Adds and returns the telemetry sensor `0010` |

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
