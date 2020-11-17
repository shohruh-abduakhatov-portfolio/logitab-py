class ChildConfig(object):
    @property
    def osrm_host(self):
        return ""


    @property
    def osrm_host_dev(self):
        return ""


    @property
    def token_client(self):
        return "4"


    @property
    def email_port(self):
        return 587


    @property
    def smtp_server(self):
        return "


    @property
    def email_from(self):
        return ""


    @property
    def email_password(self):
        return "Logitab_2020"


    @property
    def aws_access_key(self):
        return ""


    @property
    def aws_key_id(self):
        return ""


    @property
    def aws_uri(self):
        return ''


    @property
    def aws_bucket(self):
        return ''



    @property
    def aws_region_name(self):
        return 'us-west-2'


child_config = ChildConfig()
