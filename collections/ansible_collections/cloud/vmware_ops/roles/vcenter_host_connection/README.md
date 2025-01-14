# vcenter_host_connection

Add, remove, connect, disconnect, or reconnect an ESXi host from a vCenter

## Dependencies

N/A

## Role Variables

### Auth

- **vcenter_host_connection_hostname** (str, required)
    - The hostname or IP address of the vSphere vCenter.
    - If this variable is not set, the collection level variable `vmware_ops_hostname` will be used. If that variable is not set, the environment variable `VMWARE_HOST` will be used. At least one of these variables must be set to use this role.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **vcenter_host_connection_username** (str, required)
    - The vSphere vCenter username.
    - If this variable is not set, the collection level variable `vmware_ops_username` will be used. If that variable is not set, the environment variable `VMWARE_USER` will be used. At least one of these variables must be set to use this role.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **vcenter_host_connection_password** (str, required)
    - The vSphere vCenter password.
    - If this variable is not set, the collection level variable `vmware_ops_password` will be used. If that variable is not set, the environment variable `VMWARE_PASSWORD` will be used. At least one of these variables must be set to use this role.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **vcenter_host_connection_validate_certs** (bool)
    - Allows connection when SSL certificates are not valid. Set to false when certificates are not trusted.
    - If this variable is not set, the collection level variable `vmware_ops_validate_certs` will be used. If that variable is not set, the environment variable `VMWARE_VALIDATE_CERTS` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **vcenter_host_connection_port** (int or str)
    - The port used to authenticate to the vSphere vCenter that contains the cluster to configure.
    - If this variable is not set, the collection level variable `vmware_ops_port` will be used. If that variable is not set, the environment variable `VMWARE_PORT` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

### Proxy

- **vcenter_host_connection_proxy_host** (str)
    - The hostname of a proxy host that should be used for all HTTPs communication by the role.
    - The format is a hostname or an IP.
    - If this variable is not set, the collection level variable `vmware_ops_proxy_host` will be used. If that variable is not set, the environment variable `VMWARE_PROXY_HOST` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **vcenter_host_connection_proxy_port** (str or int)
    - The port of a proxy host that should be used for all HTTPs communication by the role
    - If this variable is not set, the collection level variable `vmware_ops_proxy_host` will be used. If that variable is not set, the environment variable `VMWARE_PROXY_PORT` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

### Placement

- **vcenter_host_connection_folder** (str)
    - The folder path where the ESXi host should be added.
    - Required if the cluster name is not provided

- **vcenter_host_connection_datacenter** (str, required)
    - The datacenter name where the ESXi host should be added.

- **vcenter_host_connection_cluster** (str)
    - The cluster name where the ESXi host should be added.
    - Required if the folder name is not provided

### Connection Settings

- **vcenter_host_connection_state** (str)
    - The connection state of the ESXi host that you want to set.
    - If set to `present`, add the host if host is absent, or update the location of the host if host already exists.
    - If set to `absent`, remove the host if host is present, or do nothing if host already does not exist.
    - If set to `add_or_reconnect`, add the host if it's absent else reconnect it and update the location.
    - If set to `reconnect`, then reconnect the host if it's present and update the location.
    - If set to `disconnected`, disconnect the host if the host already exists.
    - Default is `present`
    - Choices: [`present`, `absent`, `add_or_reconnect`, `reconnect`, `disconnected`]

- **vcenter_host_connection_add_connected** (bool)
    - If true then the host will be connected as soon as it's added to vCenter.

- **vcenter_host_connection_esxi_hostname** (str, required)
    - The hostname of the ESXi host that you want to manage.

- **vcenter_host_connection_esxi_username** (str)
    - The username for the ESXi host that you want to manage.
    - Required when adding the host.

- **vcenter_host_connection_esxi_password** (str)
    - The password for the ESXi host that you want to manage.
    - Required when adding the host.

- **vcenter_host_connection_esxi_ssl_thumbprint** (str)
    - The SSL thumbprint for the ESXi host that you want to manage.

- **vcenter_host_connection_fetch_ssl_thumbprint** (bool)
    - If true, the ESXi host thumbprint will be fetched and trusted prior to adding.

- **vcenter_host_connection_force_connection** (bool)
    - If true, the connection status will be forced even if the host is managed by another vCenter.

- **vcenter_host_connection_reconnect_disconnected** (bool)
    - Reconnect disconnected hosts, if the state is present and the host already exists.


## Examples

```yaml
---
- name: Add an ESXi Host To VCenter
  hosts: localhost
  roles:
    - role: cloud.vmware_ops.vcenter_host_connection
      vars:
        vcenter_host_connection_hostname: "{{ vcenter_hostname }}"
        vcenter_host_connection_username: "{{ vcenter_username }}"
        vcenter_host_connection_password: "{{ vcenter_password }}"
        vcenter_host_connection_datacenter: dc1
        vcenter_host_connection_cluster: cluster1
        vcenter_host_connection_esxi_hostname: myesxi.contoso.org
        vcenter_host_connection_esxi_username: root
        vcenter_host_connection_esxi_password: supersecret!


- name: Remove an ESXi Host From VCenter
  hosts: localhost
  roles:
    - role: cloud.vmware_ops.vcenter_host_connection
      vars:
        vcenter_host_connection_hostname: "{{ vcenter_hostname }}"
        vcenter_host_connection_username: "{{ vcenter_username }}"
        vcenter_host_connection_password: "{{ vcenter_password }}"
        vcenter_host_connection_datacenter: dc1
        vcenter_host_connection_cluster: cluster1
        vcenter_host_connection_esxi_hostname: myesxi.contoso.org
        vcenter_host_connection_state: absent
```

## License

GNU General Public License v3.0 or later

See [LICENSE](https://github.com/ansible-collections/cloud.aws_troubleshooting/blob/main/LICENSE) to see the full text.

## Author Information

- Ansible Cloud Content Team
