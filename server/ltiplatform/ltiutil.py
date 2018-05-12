def fc(claim, s=None):
    suffix = ('-'+s) if s else ''
    return 'https://purl.imsglobal.org/spec/lti{0}/claim/{1}'.format(suffix, claim)

def fdlc(claim):
    return fc(claim, s='dl')

def scope(scope, s=None):
    suffix = ('-'+s) if s else ''
    return 'https://purl.imsglobal.org/spec/lti{0}/scope/{1}'.format(suffix, scope)
    