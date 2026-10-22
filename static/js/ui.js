document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('[data-delete-confirm]');
  deleteButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
      const form = button.closest('form');
      if (!form) {
        return;
      }

      const confirmed = window.confirm('¿Deseas eliminar este elemento? Esta acción no se puede deshacer.');
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });

  const form = document.getElementById('element-form');
  if (form) {
    const saveButton = document.getElementById('save-element-btn');

    const clearFieldError = function (fieldId) {
      const node = document.getElementById(fieldId);
      if (node) {
        node.textContent = '';
      }
    };

    const showFieldError = function (fieldId, message) {
      const node = document.getElementById(fieldId);
      if (node) {
        node.textContent = message || '';
      }
    };

    const getProtocolValues = function () {
      return Array.from(document.querySelectorAll('input[name="protocols"]:checked')).map(function (checkbox) {
        return checkbox.value;
      });
    };

    const normalizeMacInput = function (value) {
      return (value || '').toString().toUpperCase().replace(/[^A-F0-9:]/g, '').slice(0, 17);
    };

    const normalizeIpInput = function (value) {
      return (value || '').toString().replace(/[^0-9.]/g, '').slice(0, 15);
    };

    const normalizeNameInput = function (value) {
      const cleaned = (value || '').toString().replace(/[^A-Za-z0-9 -]/g, '').slice(0, 50);
      if (!cleaned) {
        return cleaned;
      }
      return /^[A-Za-z]/.test(cleaned) ? cleaned : cleaned.substring(1);
    };

    const validateMac = function (value) {
      const cleaned = normalizeMacInput(value).trim();
      return /^(?:[A-F0-9]{2}:){4,5}[A-F0-9]{2}$/.test(cleaned);
    };

    const validateName = function (value) {
      return /^[A-Za-z][A-Za-z0-9 -]{0,49}$/.test((value || '').trim());
    };

    const validateIp = function (value) {
      const cleaned = normalizeIpInput(value).trim();
      if (!/^(?:\d{1,3}\.){3}\d{1,3}$/.test(cleaned)) {
        return false;
      }
      const octets = cleaned.split('.').map(function (part) {
        return Number(part);
      });
      if (!octets.every(function (part) {
        return Number.isInteger(part) && part >= 0 && part <= 255;
      })) {
        return false;
      }
      const text = cleaned;
      if (['0.0.0.0', '0.0.0.1', '255.255.255.255'].includes(text)) {
        return false;
      }
      if (octets[0] === 0 || octets[0] === 127 || (octets[0] === 169 && octets[1] === 254)) {
        return false;
      }
      if (octets[0] >= 224) {
        return false;
      }
      return true;
    };

    const validateVlanField = function (value) {
      return (value || '').trim().length > 0;
    };

    const validateVlanPorts = function (value) {
      const text = (value || '').trim();
      if (!text) {
        return false;
      }
      const items = text.split(',').map(function (part) {
        return part.trim();
      }).filter(Boolean);
      if (items.length === 0) {
        return false;
      }
      return items.every(function (item) {
        return /^(?:Gi|Fa|Se|Te|Eth|Lo|Po)\d+(?:\/\d+){1,3}$/i.test(item);
      });
    };

    const validateVlanPolicies = function (value) {
      const text = (value || '').trim();
      if (!text) {
        return false;
      }
      const allowedPolicies = ['SSH', 'ACL', 'VLAN', 'STP', 'TELNET', 'ROUTING', 'MONITORING', 'POLICY'];
      const items = text.split(',').map(function (part) {
        return part.trim().toUpperCase();
      }).filter(Boolean);
      if (items.length === 0) {
        return false;
      }
      return items.every(function (item) {
        return allowedPolicies.includes(item) || /^POL_\d{1,5}$/.test(item);
      });
    };

    const validateFormState = function () {
      let valid = true;
      clearFieldError('mac-error');
      clearFieldError('name-error');
      clearFieldError('ip-error');
      clearFieldError('protocols-error');
      clearFieldError('vlans-error');

      const macValue = document.getElementById('mac');
      if (!macValue || !macValue.value.trim()) {
        showFieldError('mac-error', 'Este campo no puede quedar vacío.');
        valid = false;
      } else if (!validateMac(macValue.value)) {
        showFieldError('mac-error', 'Los datos ingresados no son correctos.');
        valid = false;
      }

      const nameValue = document.getElementById('name');
      if (!nameValue || !nameValue.value.trim()) {
        showFieldError('name-error', 'Este campo no puede quedar vacío.');
        valid = false;
      } else if (!validateName(nameValue.value)) {
        showFieldError('name-error', 'Los datos ingresados no son correctos.');
        valid = false;
      }

      const ipValue = document.getElementById('ip');
      if (!ipValue || !ipValue.value.trim()) {
        showFieldError('ip-error', 'Este campo no puede quedar vacío.');
        valid = false;
      } else if (!validateIp(ipValue.value)) {
        showFieldError('ip-error', 'Los datos ingresados no son correctos.');
        valid = false;
      }

      if (getProtocolValues().length === 0) {
        showFieldError('protocols-error', 'Debe seleccionar al menos un protocolo.');
        valid = false;
      }

      const vlanBlocks = Array.from(document.querySelectorAll('.vlan-block'));
      for (let index = 0; index < vlanBlocks.length; index += 1) {
        const block = vlanBlocks[index];
        const fieldsInBlock = block.querySelectorAll('input');
        const values = Array.from(fieldsInBlock).map(function (input) {
          return input.value.trim();
        });
        const hasAnyContent = values.some(function (value) {
          return value.length > 0;
        });

        if (!hasAnyContent) {
          continue;
        }

        const vlanName = block.querySelector('input[name="vlan_name[]"]');
        const vlanIp = block.querySelector('input[name="vlan_ip[]"]');
        const vlanPorts = block.querySelector('input[name="vlan_ports[]"]');
        const vlanPolicies = block.querySelector('input[name="vlan_policies[]"]');

        if (!vlanName || !validateVlanField(vlanName.value)) {
          showFieldError('vlans-error', 'Cada bloque VLAN debe tener un nombre válido.');
          valid = false;
          break;
        }
        if (!vlanIp || !validateIp(vlanIp.value)) {
          showFieldError('vlans-error', 'Cada bloque VLAN debe tener una IP válida.');
          valid = false;
          break;
        }
        if (!vlanPorts || !validateVlanPorts(vlanPorts.value)) {
          showFieldError('vlans-error', 'Los puertos del VLAN no son correctos.');
          valid = false;
          break;
        }
        if (!vlanPolicies || !validateVlanPolicies(vlanPolicies.value)) {
          showFieldError('vlans-error', 'Las políticas del VLAN no son correctas.');
          valid = false;
          break;
        }
      }

      if (saveButton) {
        saveButton.disabled = !valid;
      }
      return valid;
    };

    const applyFieldFilters = function (input) {
      const fieldId = input.id || input.name;
      if (!fieldId) {
        return;
      }

      if (fieldId === 'mac') {
        input.value = normalizeMacInput(input.value);
      }

      if (fieldId === 'ip' || input.name === 'vlan_ip[]') {
        input.value = normalizeIpInput(input.value);
      }

      if (fieldId === 'name') {
        input.value = normalizeNameInput(input.value);
      }

      if (input.name === 'vlan_name[]') {
        input.value = (input.value || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 20);
      }

      if (input.name === 'vlan_ports[]') {
        input.value = (input.value || '').toString().replace(/[^A-Za-z0-9,\/\s]/g, '').replace(/\s+/g, ' ').slice(0, 60);
      }

      if (input.name === 'vlan_policies[]') {
        input.value = (input.value || '').toString().replace(/[^A-Za-z0-9_,\s]/g, '').replace(/\s+/g, ' ').slice(0, 60);
      }
    };

    const buildVlanBlock = function (data = {}) {
      const block = document.createElement('div');
      block.className = 'vlan-block';

      const vlanName = (data.vlan_name || '').toString();
      const ipv4Address = (data.ipv4_address || '').toString();
      const ports = Array.isArray(data.ports) ? data.ports.join(', ') : '';
      const policies = Array.isArray(data.policies) ? data.policies.join(', ') : '';

      const wrapper = document.createElement('div');
      wrapper.className = 'vlan-header';

      const title = document.createElement('span');
      title.textContent = 'VLAN details';

      const deleteButton = document.createElement('button');
      deleteButton.type = 'button';
      deleteButton.className = 'remove-vlan';
      deleteButton.textContent = 'Remove';
      deleteButton.addEventListener('click', function () {
        const allBlocks = document.querySelectorAll('.vlan-block');
        if (allBlocks.length > 1) {
          block.remove();
          validateFormState();
        }
      });

      wrapper.appendChild(title);
      wrapper.appendChild(deleteButton);

      const grid = document.createElement('div');
      grid.className = 'vlan-grid';

      const fieldMap = [
        ['vlan_name[]', vlanName, 'VL1'],
        ['vlan_ip[]', ipv4Address, '192.168.27.171'],
        ['vlan_ports[]', ports, 'Gi0/0, Gi0/1'],
        ['vlan_policies[]', policies, 'POL_174, SSH']
      ];

      fieldMap.forEach(function (entry) {
        const [name, value, placeholder] = entry;
        const wrapperField = document.createElement('div');
        const label = document.createElement('label');
        label.textContent = name === 'vlan_name[]' ? 'VLAN name' : name === 'vlan_ip[]' ? 'IPv4' : name === 'vlan_ports[]' ? 'Ports' : 'Policies';

        const input = document.createElement('input');
        input.type = 'text';
        input.name = name;
        input.value = value || '';
        input.placeholder = placeholder;
        input.addEventListener('input', function () {
          applyFieldFilters(input);
          validateFormState();
        });

        wrapperField.appendChild(label);
        wrapperField.appendChild(input);
        grid.appendChild(wrapperField);
      });

      block.appendChild(wrapper);
      block.appendChild(grid);
      return block;
    };

    const addButton = document.getElementById('add-vlan-btn');
    const container = document.getElementById('vlan-container');

    if (addButton && container) {
      addButton.addEventListener('click', function () {
        const newBlock = buildVlanBlock();
        container.appendChild(newBlock);
        validateFormState();
        const firstInput = newBlock.querySelector('input[name="vlan_name[]"]');
        if (firstInput) {
          firstInput.focus();
          firstInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }

    const fields = ['mac', 'name', 'status', 'ip'];
    fields.forEach(function (fieldName) {
      const field = document.getElementById(fieldName);
      if (field) {
        field.addEventListener('input', function () {
          applyFieldFilters(field);
          validateFormState();
        });
      }
    });

    document.querySelectorAll('input[name="protocols"]').forEach(function (checkbox) {
      checkbox.addEventListener('change', validateFormState);
    });

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!validateFormState()) {
        return;
      }

      const formData = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': formData.get('csrf_token')
        },
        credentials: 'same-origin'
      }).then(function (response) {
        if (response.redirected) {
          window.location.href = response.url;
          return;
        }
        if (response.ok) {
          const toast = document.createElement('div');
          toast.className = 'toast toast-success';
          toast.textContent = 'Elemento guardado correctamente';
          document.body.appendChild(toast);
          setTimeout(function () {
            toast.classList.add('is-visible');
          }, 10);
          setTimeout(function () {
            toast.classList.remove('is-visible');
            setTimeout(function () {
              toast.remove();
              window.location.href = '/tabla_elementos';
            }, 220);
          }, 1500);
          return;
        }

        return response.json().then(function (payload) {
          const errors = Array.isArray(payload) ? payload : [payload];
          const knownFields = ['mac', 'name', 'status', 'ip', 'protocols', 'vlan_name', 'vlan_ip', 'ports', 'policies'];
          knownFields.forEach(function (field) {
            clearFieldError(field + '-error');
          });

          errors.forEach(function (item) {
            const field = item.field || 'general';
            const id = field === 'vlan_name' || field === 'vlan_ip' || field === 'ports' || field === 'policies' ? 'vlans-error' : field + '-error';
            showFieldError(id, item.message || 'Invalid value.');
          });
        });
      }).catch(function () {
        showFieldError('general-error', 'Request failed.');
      });
    });

    validateFormState();
  }
});
