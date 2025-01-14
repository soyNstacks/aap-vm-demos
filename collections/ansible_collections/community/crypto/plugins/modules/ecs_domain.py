#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 Entrust Datacard Corporation.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r"""
module: ecs_domain
author:
  - Chris Trufan (@ctrufan)
version_added: '1.0.0'
short_description: Request validation of a domain with the Entrust Certificate Services (ECS) API
description:
  - Request validation or re-validation of a domain with the Entrust Certificate Services (ECS) API.
  - Requires credentials for the L(Entrust Certificate Services,https://www.entrustdatacard.com/products/categories/ssl-certificates)
    (ECS) API.
  - If the domain is already in the validation process, no new validation will be requested, but the validation data (if applicable)
    will be returned.
  - If the domain is already in the validation process but the O(verification_method) specified is different than the current
    O(verification_method), the O(verification_method) will be updated and validation data (if applicable) will be returned.
  - If the domain is an active, validated domain, the return value of C(changed) will be false, unless RV(domain_status=EXPIRED),
    in which case a re-validation will be performed.
  - If O(verification_method=dns), details about the required DNS entry will be specified in the return parameters RV(dns_contents),
    RV(dns_location), and RV(dns_resource_type).
  - If O(verification_method=web_server), details about the required file details will be specified in the return parameters
    RV(file_contents) and RV(file_location).
  - If O(verification_method=email), the email address(es) that the validation email(s) were sent to will be in the return
    parameter RV(emails). This is purely informational. For domains requested using this module, this will always be a list
    of size 1.
notes:
  - There is a small delay (typically about 5 seconds, but can be as long as 60 seconds) before obtaining the random values
    when requesting a validation while O(verification_method=dns) or O(verification_method=web_server). Be aware of that if
    doing many domain validation requests.
extends_documentation_fragment:
  - community.crypto.attributes
  - community.crypto.ecs_credential
attributes:
  check_mode:
    support: none
  diff_mode:
    support: none
  idempotent:
    support: partial
    details:
      - Under which conditions the module is idempotent still needs to be determined.
        If you are using this module and have more information, please contribute to
        the documentation!
options:
  client_id:
    description:
      - The client ID to request the domain be associated with.
      - If no client ID is specified, the domain will be added under the primary client with ID of 1.
    type: int
    default: 1
  domain_name:
    description:
      - The domain name to be verified or reverified.
    type: str
    required: true
  verification_method:
    description:
      - The verification method to be used to prove control of the domain.
      - If O(verification_method=email) and the value O(verification_email) is specified, that value is used for the email
        validation. If O(verification_email) is not provided, the first value present in WHOIS data will be used. An email
        will be sent to the address in O(verification_email) with instructions on how to verify control of the domain.
      - If O(verification_method=dns), the value RV(dns_contents) must be stored in location RV(dns_location), with a DNS
        record type of RV(dns_resource_type). To prove domain ownership, update your DNS records so the text string returned
        by RV(dns_contents) is available at RV(dns_location).
      - If O(verification_method=web_server), the contents of return value RV(file_contents) must be made available on a web
        server accessible at location RV(file_location).
      - If O(verification_method=manual), the domain will be validated with a manual process. This is not recommended.
    type: str
    choices: ['dns', 'email', 'manual', 'web_server']
    required: true
  verification_email:
    description:
      - Email address to be used to verify domain ownership.
      - 'Email address must be either an email address present in the WHOIS data for O(domain_name), or one of the following
        constructed emails: admin@O(domain_name), administrator@O(domain_name), webmaster@O(domain_name), hostmaster@O(domain_name),
        postmaster@O(domain_name).'
      - Note that if O(domain_name) includes subdomains, the top level domain should be used. For example, if requesting validation
        of example1.ansible.com, or test.example2.ansible.com, and you want to use the "admin" preconstructed name, the email
        address should be admin@ansible.com.
      - If using the email values from the WHOIS data for the domain or its top level namespace, they must be exact matches.
      - If O(verification_method=email) but O(verification_email) is not provided, the first email address found in WHOIS
        data for the domain will be used.
      - To verify domain ownership, domain owner must follow the instructions in the email they receive.
      - Only allowed if O(verification_method=email).
    type: str
seealso:
  - module: community.crypto.x509_certificate
    description: Can be used to request certificates from ECS, with O(community.crypto.x509_certificate#module:provider=entrust).
  - module: community.crypto.ecs_certificate
    description: Can be used to request a Certificate from ECS using a verified domain.
"""

EXAMPLES = r"""
- name: Request domain validation using email validation for client ID of 2.
  community.crypto.ecs_domain:
    domain_name: ansible.com
    client_id: 2
    verification_method: email
    verification_email: admin@ansible.com
    entrust_api_user: apiusername
    entrust_api_key: a^lv*32!cd9LnT
    entrust_api_client_cert_path: /etc/ssl/entrust/ecs-client.crt
    entrust_api_client_cert_key_path: /etc/ssl/entrust/ecs-client.key

- name: Request domain validation using DNS. If domain is already valid, request revalidation if expires within 90 days
  community.crypto.ecs_domain:
    domain_name: ansible.com
    verification_method: dns
    entrust_api_user: apiusername
    entrust_api_key: a^lv*32!cd9LnT
    entrust_api_client_cert_path: /etc/ssl/entrust/ecs-client.crt
    entrust_api_client_cert_key_path: /etc/ssl/entrust/ecs-client.key

- name: Request domain validation using web server validation, and revalidate if fewer than 60 days remaining of EV eligibility.
  community.crypto.ecs_domain:
    domain_name: ansible.com
    verification_method: web_server
    entrust_api_user: apiusername
    entrust_api_key: a^lv*32!cd9LnT
    entrust_api_client_cert_path: /etc/ssl/entrust/ecs-client.crt
    entrust_api_client_cert_key_path: /etc/ssl/entrust/ecs-client.key

- name: Request domain validation using manual validation.
  community.crypto.ecs_domain:
    domain_name: ansible.com
    verification_method: manual
    entrust_api_user: apiusername
    entrust_api_key: a^lv*32!cd9LnT
    entrust_api_client_cert_path: /etc/ssl/entrust/ecs-client.crt
    entrust_api_client_cert_key_path: /etc/ssl/entrust/ecs-client.key
"""

RETURN = r"""
domain_status:
  description: Status of the current domain. Will be one of V(APPROVED), V(DECLINED), V(CANCELLED), V(INITIAL_VERIFICATION),
    V(DECLINED), V(CANCELLED), V(RE_VERIFICATION), V(EXPIRED), V(EXPIRING).
  returned: changed or success
  type: str
  sample: APPROVED
verification_method:
  description: Verification method used to request the domain validation. If C(changed) will be the same as O(verification_method)
    input parameter.
  returned: changed or success
  type: str
  sample: dns
file_location:
  description: The location that ECS will be expecting to be able to find the file for domain verification, containing the
    contents of RV(file_contents).
  returned: O(verification_method) is V(web_server)
  type: str
  sample: http://ansible.com/.well-known/pki-validation/abcd.txt
file_contents:
  description: The contents of the file that ECS will be expecting to find at RV(file_location).
  returned: O(verification_method) is V(web_server)
  type: str
  sample: AB23CD41432522FF2526920393982FAB
emails:
  description:
    - The list of emails used to request validation of this domain.
    - Domains requested using this module will only have a list of size 1.
  returned: O(verification_method) is V(email)
  type: list
  sample: [admin@ansible.com, administrator@ansible.com]
dns_location:
  description: The location that ECS will be expecting to be able to find the DNS entry for domain verification, containing
    the contents of RV(dns_contents).
  returned: changed and if O(verification_method) is V(dns)
  type: str
  sample: _pki-validation.ansible.com
dns_contents:
  description: The value that ECS will be expecting to find in the DNS record located at RV(dns_location).
  returned: changed and if O(verification_method) is V(dns)
  type: str
  sample: AB23CD41432522FF2526920393982FAB
dns_resource_type:
  description: The type of resource record that ECS will be expecting for the DNS record located at RV(dns_location).
  returned: changed and if O(verification_method) is V(dns)
  type: str
  sample: TXT
client_id:
  description: Client ID that the domain belongs to. If the input value O(client_id) is specified, this will always be the
    same as O(client_id).
  returned: changed or success
  type: int
  sample: 1
ov_eligible:
  description: Whether the domain is eligible for submission of "OV" certificates. Will never be V(false) if RV(ev_eligible)
    is V(true).
  returned: success and RV(domain_status) is V(APPROVED), V(RE_VERIFICATION), V(EXPIRING), or V(EXPIRED).
  type: bool
  sample: true
ov_days_remaining:
  description: The number of days the domain remains eligible for submission of "OV" certificates. Will never be less than
    the value of RV(ev_days_remaining).
  returned: success and RV(ov_eligible) is V(true) and RV(domain_status) is V(APPROVED), V(RE_VERIFICATION) or V(EXPIRING).
  type: int
  sample: 129
ev_eligible:
  description: Whether the domain is eligible for submission of "EV" certificates. Will never be V(true) if RV(ov_eligible)
    is V(false).
  returned: success and RV(domain_status) is V(APPROVED), V(RE_VERIFICATION) or V(EXPIRING), or V(EXPIRED).
  type: bool
  sample: true
ev_days_remaining:
  description: The number of days the domain remains eligible for submission of "EV" certificates. Will never be greater than
    the value of RV(ov_days_remaining).
  returned: success and RV(ev_eligible) is V(true) and RV(domain_status) is V(APPROVED), V(RE_VERIFICATION) or V(EXPIRING).
  type: int
  sample: 94
"""

import datetime
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

from ansible_collections.community.crypto.plugins.module_utils.ecs.api import (
    ecs_client_argument_spec,
    ECSClient,
    RestOperationException,
    SessionConfigurationException,
)


def calculate_days_remaining(expiry_date):
    days_remaining = None
    if expiry_date:
        expiry_datetime = datetime.datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%SZ')
        days_remaining = (expiry_datetime - datetime.datetime.now()).days
    return days_remaining


class EcsDomain(object):
    '''
    Entrust Certificate Services domain class.
    '''

    def __init__(self, module):
        self.changed = False
        self.domain_status = None
        self.verification_method = None
        self.file_location = None
        self.file_contents = None
        self.dns_location = None
        self.dns_contents = None
        self.dns_resource_type = None
        self.emails = None
        self.ov_eligible = None
        self.ov_days_remaining = None
        self.ev_eligble = None
        self.ev_days_remaining = None
        # Note that verification_method is the 'current' verification
        # method of the domain, we'll use module.params when requesting a new
        # one, in case the verification method has changed.
        self.verification_method = None

        self.ecs_client = None
        # Instantiate the ECS client and then try a no-op connection to verify credentials are valid
        try:
            self.ecs_client = ECSClient(
                entrust_api_user=module.params['entrust_api_user'],
                entrust_api_key=module.params['entrust_api_key'],
                entrust_api_cert=module.params['entrust_api_client_cert_path'],
                entrust_api_cert_key=module.params['entrust_api_client_cert_key_path'],
                entrust_api_specification_path=module.params['entrust_api_specification_path']
            )
        except SessionConfigurationException as e:
            module.fail_json(msg='Failed to initialize Entrust Provider: {0}'.format(to_native(e)))
        try:
            self.ecs_client.GetAppVersion()
        except RestOperationException as e:
            module.fail_json(msg='Please verify credential information. Received exception when testing ECS connection: {0}'.format(to_native(e.message)))

    def set_domain_details(self, domain_details):
        if domain_details.get('verificationMethod'):
            self.verification_method = domain_details['verificationMethod'].lower()
        self.domain_status = domain_details['verificationStatus']
        self.ov_eligible = domain_details.get('ovEligible')
        self.ov_days_remaining = calculate_days_remaining(domain_details.get('ovExpiry'))
        self.ev_eligible = domain_details.get('evEligible')
        self.ev_days_remaining = calculate_days_remaining(domain_details.get('evExpiry'))
        self.client_id = domain_details['clientId']

        if self.verification_method == 'dns' and domain_details.get('dnsMethod'):
            self.dns_location = domain_details['dnsMethod']['recordDomain']
            self.dns_resource_type = domain_details['dnsMethod']['recordType']
            self.dns_contents = domain_details['dnsMethod']['recordValue']
        elif self.verification_method == 'web_server' and domain_details.get('webServerMethod'):
            self.file_location = domain_details['webServerMethod']['fileLocation']
            self.file_contents = domain_details['webServerMethod']['fileContents']
        elif self.verification_method == 'email' and domain_details.get('emailMethod'):
            self.emails = domain_details['emailMethod']

    def check(self, module):
        try:
            domain_details = self.ecs_client.GetDomain(clientId=module.params['client_id'], domain=module.params['domain_name'])
            self.set_domain_details(domain_details)
            if self.domain_status != 'APPROVED' and self.domain_status != 'INITIAL_VERIFICATION' and self.domain_status != 'RE_VERIFICATION':
                return False

            # If domain verification is in process, we want to return the random values and treat it as a valid.
            if self.domain_status == 'INITIAL_VERIFICATION' or self.domain_status == 'RE_VERIFICATION':
                # Unless the verification method has changed, in which case we need to do a reverify request.
                if self.verification_method != module.params['verification_method']:
                    return False

            if self.domain_status == 'EXPIRING':
                return False

            return True
        except RestOperationException as dummy:
            return False

    def request_domain(self, module):
        if not self.check(module):
            body = {}

            body['verificationMethod'] = module.params['verification_method'].upper()
            if module.params['verification_method'] == 'email':
                emailMethod = {}
                if module.params['verification_email']:
                    emailMethod['emailSource'] = 'SPECIFIED'
                    emailMethod['email'] = module.params['verification_email']
                else:
                    emailMethod['emailSource'] = 'INCLUDE_WHOIS'
                body['emailMethod'] = emailMethod
            # Only populate domain name in body if it is not an existing domain
            if not self.domain_status:
                body['domainName'] = module.params['domain_name']
            try:
                if not self.domain_status:
                    self.ecs_client.AddDomain(clientId=module.params['client_id'], Body=body)
                else:
                    self.ecs_client.ReverifyDomain(clientId=module.params['client_id'], domain=module.params['domain_name'], Body=body)

                time.sleep(5)
                result = self.ecs_client.GetDomain(clientId=module.params['client_id'], domain=module.params['domain_name'])

                # It takes a bit of time before the random values are available
                if module.params['verification_method'] == 'dns' or module.params['verification_method'] == 'web_server':
                    for i in range(4):
                        # Check both that random values are now available, and that they're different than were populated by previous 'check'
                        if module.params['verification_method'] == 'dns':
                            if result.get('dnsMethod') and result['dnsMethod']['recordValue'] != self.dns_contents:
                                break
                        elif module.params['verification_method'] == 'web_server':
                            if result.get('webServerMethod') and result['webServerMethod']['fileContents'] != self.file_contents:
                                break
                    time.sleep(10)
                    result = self.ecs_client.GetDomain(clientId=module.params['client_id'], domain=module.params['domain_name'])
                self.changed = True
                self.set_domain_details(result)
            except RestOperationException as e:
                module.fail_json(msg='Failed to request domain validation from Entrust (ECS) {0}'.format(e.message))

    def dump(self):
        result = {
            'changed': self.changed,
            'client_id': self.client_id,
            'domain_status': self.domain_status,
        }

        if self.verification_method:
            result['verification_method'] = self.verification_method
        if self.ov_eligible is not None:
            result['ov_eligible'] = self.ov_eligible
        if self.ov_days_remaining:
            result['ov_days_remaining'] = self.ov_days_remaining
        if self.ev_eligible is not None:
            result['ev_eligible'] = self.ev_eligible
        if self.ev_days_remaining:
            result['ev_days_remaining'] = self.ev_days_remaining
        if self.emails:
            result['emails'] = self.emails

        if self.verification_method == 'dns':
            result['dns_location'] = self.dns_location
            result['dns_contents'] = self.dns_contents
            result['dns_resource_type'] = self.dns_resource_type
        elif self.verification_method == 'web_server':
            result['file_location'] = self.file_location
            result['file_contents'] = self.file_contents
        elif self.verification_method == 'email':
            result['emails'] = self.emails

        return result


def ecs_domain_argument_spec():
    return dict(
        client_id=dict(type='int', default=1),
        domain_name=dict(type='str', required=True),
        verification_method=dict(type='str', required=True, choices=['dns', 'email', 'manual', 'web_server']),
        verification_email=dict(type='str'),
    )


def main():
    ecs_argument_spec = ecs_client_argument_spec()
    ecs_argument_spec.update(ecs_domain_argument_spec())
    module = AnsibleModule(
        argument_spec=ecs_argument_spec,
        supports_check_mode=False,
    )

    if module.params['verification_email'] and module.params['verification_method'] != 'email':
        module.fail_json(msg='The verification_email field is invalid when verification_method="{0}".'.format(module.params['verification_method']))

    domain = EcsDomain(module)
    domain.request_domain(module)
    result = domain.dump()
    module.exit_json(**result)


if __name__ == '__main__':
    main()