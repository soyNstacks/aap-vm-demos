# deploy_ovf

A role to deploy a VM from an OVF file. The OVF can be located on the `ansible_host` filesystem, at a URL, or located in a content library.

## Dependencies

N/A

## Role Variables

### Auth

- **deploy_ovf_hostname** (str, required)
    - The hostname or IP address of the vSphere vCenter or ESXi host.
    - If this variable is not set, the collection level variable `vmware_ops_hostname` will be used. If that variable is not set, the environment variable `VMWARE_HOST` will be used. At least one of these variables must be set to use this role.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **deploy_ovf_username** (str, required)
    - The vSphere vCenter or ESXi host username.
    - If this variable is not set, the collection level variable `vmware_ops_username` will be used. If that variable is not set, the environment variable `VMWARE_USER` will be used. At least one of these variables must be set to use this role.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **deploy_ovf_password** (str, required)
    - The vSphere vCenter or ESXi host password.
    - If this variable is not set, the collection level variable `vmware_ops_password` will be used. If that variable is not set, the environment variable `VMWARE_PASSWORD` will be used. At least one of these variables must be set to use this role.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **deploy_ovf_validate_certs** (bool)
    - Allows connection when SSL certificates are not valid. Set to false when certificates are not trusted.
    - If this variable is not set, the collection level variable `vmware_ops_validate_certs` will be used. If that variable is not set, the environment variable `VMWARE_VALIDATE_CERTS` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **deploy_ovf_port** (int or str)
    - The port used to authenticate to the vSphere vCenter or ESXi host.
    - If this variable is not set, the collection level variable `vmware_ops_port` will be used. If that variable is not set, the environment variable `VMWARE_PORT` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

### Proxy

- **deploy_ovf_proxy_host** (str)
    - The hostname of a proxy host that should be used for all HTTPs communication by the role.
    - The format is a hostname or an IP.
    - If this variable is not set, the collection level variable `vmware_ops_proxy_host` will be used. If that variable is not set, the environment variable `VMWARE_PROXY_HOST` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

- **deploy_ovf_proxy_port** (str or int)
    - The port of a proxy host that should be used for all HTTPs communication by the role
    - If this variable is not set, the collection level variable `vmware_ops_proxy_host` will be used. If that variable is not set, the environment variable `VMWARE_PROXY_PORT` will be used.
    - See the [authentication documentation](https://github.com/redhat-cop/cloud.vmware_ops/blob/main/docs/authentication.md) for examples.

### Placement

- **deploy_ovf_cluster_name** (str)
    - The name of the cluster in vSphere vCenter to configure.
    - Required if you are connecting to a vCenter cluster and `deploy_ovf_esxi_host` is not provided.

- **deploy_ovf_datacenter_name** (str, required)
    - The name of the datacenter in vSphere vCenter where the virtual machine should be deployed.

- **deploy_ovf_datastore** (str)
    - The name of the datastore that the virtual machine should use for storage.
    - Required unless `deploy_ovf_datastore_cluster` is defined and `deploy_ovf_library` is defined.

- **deploy_ovf_esxi_host** (str)
    - The ESXi hostname where the virtual machine will run.
    - Required if `deploy_ovf_cluster_name` is not provided.

- **deploy_ovf_resource_pool** (str)
    - The name of the resource pool where the virtual machine will be deployed.

### Deployment settings

- **deploy_ovf_vm_name** (str, required)
    - The name of the virtual machine to deploy.

- **deploy_ovf_template** (str)
    - The name or path of the OVF template to deploy.
    - Required unless `deploy_ovf_url` is defined.
    - If `deploy_ovf_library` is not defined, this should be the absolute path on the `ansible_host` filesystem to the OVF file
    - If `deploy_ovf_library` is defined, this should be the path or name of the template in the content library to the OVF file

- **deploy_ovf_url** (str)
    - The url to the OVF file. The file will be downloaded on the remote host and deployed.
    - Mutually exclusive with `deploy_ovf_template` and `deploy_ovf_library`

- **deploy_ovf_library** (str)
    - The name of the content library that contains the OVF file.
    - Mutually exclusive with `deploy_ovf_url`

#### Local Filesystem/URL

- **deploy_ovf_allow_duplicates** (bool)
    - Whether or not to allow duplicate VM names. ESXi allows duplicates, vCenter may not.

- **deploy_ovf_deployment_option** (str)
    - The key of the chosen deployment option

- **deploy_ovf_disk_provisioning** (str)
    - The disk provisioning type to use
    - Choices: [`flat`, `eagerZeroedThick`, `monolithicSparse`, `twoGbMaxExtentSparse`, `twoGbMaxExtentFlat`, `thin`, `sparse`, `thick`, `seSparse`, `monolithicFlat`]

- **deploy_ovf_enable_hidden_properties** (bool)
    - Enable source properties that are marked as ovf:userConfigurable=false

- **deploy_ovf_fail_on_spec_warnings** (bool)
    - Cause the module to treat OVF Import Spec warnings as errors.

- **deploy_ovf_inject_ovf_env** (bool)
    - Force the given properties to be inserted into an OVF Environment and injected through VMware Tools.

- **deploy_ovf_networks** (dict)
    - Mapping of OVF network name to the vCenter network name

- **deploy_ovf_power_on** (bool)
    - Whether or not to power on the virtual machine after creation.

- **deploy_ovf_properties** (dict)
    - The assignment of values to the properties found in the OVF as key value pairs.

- **deploy_ovf_wait** (bool)
    - Wait for the host to power on.

- **deploy_ovf_wait_for_ip_address** (bool)
    - Wait until vCenter detects an IP address for the VM. This requires vmware-tools (vmtoolsd) to properly work after creation.

#### Content Library

- **deploy_ovf_datastore_cluster** (str)
    - The name of the datastore cluster to use as storage for the VM.
    - If no `deploy_ovf_datastore` is set, the default datastore for the cluster will be used. Otherwise `deploy_ovf_datastore` must exist in the datastore cluster.

- **deploy_ovf_log_level** (str)
    - The log level to use for the module.
    - Choices: [`normal`, `info`, `debug`]

- **deploy_ovf_storage_provisioning** (str)
    - Default storage provisioning type to use for all sections of type vmw:StorageSection in the OVF descriptor.
    - Choices: [`thin`, `thick`, `eagerZeroedThick`, `eagerzeroedthick`]

## Examples

```yaml
---
- name: Deploy OVF From URL
  hosts: all
  gather_facts: false

  roles:
    - role: cloud.vmware_ops.deploy_ovf
      deploy_ovf_hostname: <>
      deploy_ovf_username: <>
      deploy_ovf_password: <>
      deploy_ovf_datacenter_name: DC1
      deploy_ovf_cluster_name: CL1
      deploy_ovf_vm_name: test-vm
      deploy_ovf_url: https://example.com/ovf
      deploy_ovf_datastore: datastore1

- name: Deploy OVF From Library
  hosts: all
  gather_facts: false

  roles:
    - role: cloud.vmware_ops.deploy_ovf
      deploy_ovf_hostname: <>
      deploy_ovf_username: <>
      deploy_ovf_password: <>
      deploy_ovf_datacenter_name: DC1
      deploy_ovf_cluster_name: CL1
      deploy_ovf_vm_name: test-vm
      deploy_ovf_library: my-content-library
      deploy_ovf_template: my-ovf-template
      deploy_ovf_datastore: datastore1

- name: Deploy OVF From Filesystem
  hosts: all
  gather_facts: false

  roles:
    - role: cloud.vmware_ops.deploy_ovf
      deploy_ovf_hostname: <>
      deploy_ovf_username: <>
      deploy_ovf_password: <>
      deploy_ovf_datacenter_name: DC1
      deploy_ovf_cluster_name: CL1
      deploy_ovf_vm_name: test-vm
      deploy_ovf_template: /opt/ovfs/my-ovf-template.ovf
      deploy_ovf_datastore: datastore1
```

## License

GNU General Public License v3.0 or later

See [LICENSE](https://github.com/ansible-collections/cloud.aws_troubleshooting/blob/main/LICENSE) to see the full text.

## Author Information

- Ansible Cloud Content Team
