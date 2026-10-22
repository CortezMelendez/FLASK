import app


def test_mac_and_name_validation():
    form = {
        'mac': 'AA::10C::7D::01',
        'name': 'Router1',
        'ip': '192.168.27.171',
        'status': 'online',
        'protocols': ['STP', 'OSPF'],
        'vlan_name[]': ['VL1'],
        'vlan_ip[]': ['192.168.27.171'],
        'vlan_ports[]': ['Gi0/0, Gi0/1'],
        'vlan_policies[]': ['POL_174'],
    }
    payload, errors = app.validate_element_form(form)
    assert not errors, errors
    assert payload['mac'] == 'AA:10C:7D:01'
    assert payload['protocols'] == ['STP', 'OSPF']


def test_invalid_protocols_and_sql_guard():
    form = {
        'mac': 'AA:BB:CC:DD:EE:FF',
        'name': 'DROP TABLE users',
        'ip': '192.168.1.1',
        'status': 'online',
        'protocols': ['BAD'],
        'vlan_name[]': ['VL1'],
        'vlan_ip[]': ['192.168.1.2'],
        'vlan_ports[]': ['Gi0/0'],
        'vlan_policies[]': ['SSH'],
    }
    payload, errors = app.validate_element_form(form)
    assert payload is None
    assert any(error['field'] == 'name' for error in errors)
    assert any(error['field'] == 'protocols' for error in errors)
