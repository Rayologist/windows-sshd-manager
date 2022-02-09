import argparse
from pathlib import Path


class WSMParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Windows SSHD Manager",
            description="Manage Windows OpenSSH Log",
        )

        self.subparser = self.parser.add_subparsers(
            dest="subcmd",
            help="description",
            metavar="Actions",
            required=True
        )
        
        self.add_config_subparser()
        self.add_start_parser()
        self.add_ban_subparser()
        self.add_whois_parser()
        self.add_status_parser()
        self.add_allow_parser()
        self.add_deny_parser()
        self.add_report_parser()
        

    def add_report_parser(self):
        report = self.subparser.add_parser(
            "report",
            help="Generate report for sshd status"
        )

        report.add_argument(
            "-y", "--yesterday",
            help="Get report of yesterday",
            action="store_true"
        )

        report.add_argument(
            "-d", "--day",
            help="Get report of the given day",
            type=str
        )

        report.add_argument(
            "-r", "--range",
            nargs="+",
            help="Display report of the given date range"
        )

        report.add_argument(
            "--group-by",
            type=str,
            choices=['ip', 'username', 'country'],
            help="Group data by the given column"
        )

        report.add_argument(
            "--table",
            type=str,
            choices=["failed", 'success', 'banned'],
            default="failed",
            help="Group data by the given column"
        )

        report.add_argument(
            "--save-path",
            type=Path,
            help="Save report to the given path"
        )
    

    def add_deny_parser(self):
        deny = self.subparser.add_parser(
            "deny",
            help="Deny ips from access forever"
        )

        deny.add_argument(
            dest="deny",
            nargs="+",
        )

        deny.add_argument(
            "--lift",
            action="store_true",
            help="Lift deny on ips"
        )
    
    def add_allow_parser(self):
        allow = self.subparser.add_parser(
            "allow",
            help="Deny ips from access forever"
        )

        allow.add_argument(
            dest="allow",
            nargs="+",
        )

        allow.add_argument(
            "--lift",
            action="store_true",
            help="Lift allow on ips"
        )

    def add_start_parser(self):
        start = self.subparser.add_parser(
            "start",
            help="Start wsm service"
        )

        start.add_argument(
            dest="start",
            action="store_true",
            help="Start wsm service"
        )

    def add_status_parser(self):
        status = self.subparser.add_parser(
            "status",
            help="Display wsm status"
        )

        status.add_argument(
            dest="status",
            action="store_true",
            help="Display wsm status"
        )
    
    def add_whois_parser(self):
        whois = self.subparser.add_parser(
            'whois',
            help="get whois ips",
            
        )

        whois.add_argument(
            dest='whois',
            nargs="+"
        )

        whois.add_argument(
            "--no-cache",
            action="store_true"
        )

        whois.add_argument(
            "--save-path",
            type=Path
        )

        whois.add_argument(
            "--format",
            type=str
        )

    def add_ban_subparser(self):
        ban = self.subparser.add_parser(
            'ban',
            help="ban ips"
        )

        ban.add_argument(
            dest="ban",
            nargs="+",
            help='ban ips'
        )
        
        ban.add_argument(
            '--expire',
            type=str
        )
        ban.add_argument(
            '--get',
            action="store_true"
        )

        ban.add_argument(
            '--lift',
            action="store_true"
        )

    def add_config_subparser(self):
        config = self.subparser.add_parser(
            'config',
            help="Configure windows sshd manager"
        )

        subconfig = config.add_subparsers(
            dest="subconfig",
            help="description",
            metavar="Actions",
            required=True
        )


        set_subconfig = subconfig.add_parser(
            'set',
            help="Setter for config"
        )

        set_subconfig.add_argument(
            "--log-path",
            type=Path,
            help='register sshd.log path'
        )
        
        set_subconfig.add_argument(
            "--ban-time",
            type=int,
            help='How long a failed will be banned'
        )

        set_subconfig.add_argument(
            "--find-time",
            type=int,
            help='Within how much time login errors should be counted'
        )

        set_subconfig.add_argument(
            "--max-retry",
            type=int,
            help='An ip will be banned if the error count exceeds max retry'
        )

        get_subconfig = subconfig.add_parser(
            'get',
            help="Getter for config"
        )

        get_subconfig.add_argument(
            "--log-path",
            action="store_true",
            help='Get sshd.log path'
        )
        
        get_subconfig.add_argument(
            "--ban-time",
            action="store_true",
            help='Get ban time'
        )

        get_subconfig.add_argument(
            "--find-time",
            action="store_true",
            help='Get find time'
        )

        get_subconfig.add_argument(
            "--max-retry",
            action="store_true",
            help='Get max retry'
        )
        get_subconfig.add_argument(
            "--all",
            action="store_true",
            help='Get all config'
        )
        
    def parse_args(self):
        return self.parser.parse_args()

    def error(self, message: str):
        return self.parser.error(message)

if __name__ == '__main__':
    wsm_parser = WSMParser()
    res = wsm_parser.parse_args()
    print(res)