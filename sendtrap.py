#!/usr/bin/python3

# https://python.hotexamples.com/examples/ansible.module_utils.basic/AnsibleModule/run_command/python-ansiblemodule-run_command-method-examples.html


ANSIBLE_METADATA = {
    'metadata_version': '2.10',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: sendtrap

short_description: A simple module to send an SNMPtrap

version_added: "1.00"

description:
    - "a simple module to send an SNMPtrap"

options:
    community:
        description:
            - The snmp community string
        required: false
        default: public
    target:
        description:
            - The target to sent the trap to
        required: true
    oid:
        description:
            - The SNMP OID to use
        required: false
        default: 1.3.6.1.4.1.3267
    trap:
        description:
            - The specific trap to send
        required: true
    trapmessage:
        description:
            - The trap message to send
        required: true

author:
    - Paul Ready (@lxtwin)
'''

EXAMPLES = '''
# Send a snmp trap
- name: "Send a SNMPtrap"
  sendtrap:
    target: 192.168.1.117
    trap: 6.0
    trapmessage: "Backup starting"

# Send a snmp trap
- name: "Send a SNMPtrap"
  sendtrap:
    target: lxhome@paulsdomain.com
    trap: 6.33
    trapmessage: "VCS Failed"
    community: "MyPublic"

'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define the available arguments/parameters that a user can pass to

    # the module
    module_args = dict(
        community=dict(type='str',   required=False, default="public"),
        target=dict(type='str',      required=True),
        oid=dict(type='str',         required=False, default='1.3.6.1.4.1.3267'),
        trap=dict(type='str',        required=True),
        trapmessage=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    # snmptrap -v 2c -c public 192.168.1.117  '' 1.3.6.1.4.1.3266 1.3.6.1.4.1.3267.6.0 s "The default message"

    community   = module.params['community']
    target      = module.params['target']
    oid         = module.params['oid']
    trap        = module.params['trap']
    trapmessage = module.params['trapmessage']

    trap_result = module.run_command('snmptrap -v 2c -c "%s" "%s" \'\' "%s" "%s"."%s" s "%s"' %(community, target, oid, oid, trap, trapmessage))

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['target']:
        result['debug'] = trap_result
        result['rc'] = trap_result[0]
        if result['rc']:
            result['failed'] = True
            module.fail_json(msg='Failed to sand a SNMPtrap', **result)
        else:
            result['changed'] = True
            module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
