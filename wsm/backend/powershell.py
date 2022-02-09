import subprocess
from functools import wraps
from typing import Optional, Iterable


class PowerShell1:
    def __init__(self):
        self.name: str = "wsm"

    def run(self, script: str) -> Optional[str]:
        run_result: subprocess.CompletedProcess = subprocess.run(
            ["powershell", script], capture_output=True, encoding="utf-8"
        )
        if run_result.returncode != 0:
            raise Exception(run_result.stderr)
        return run_result.stdout

    def block_ips(self, ips: Iterable[str]):
        concat_ips: str = ", ".join(map(lambda x: f"'{x}'", ips))
        script: str = (
            f"[string[]] $ips = {concat_ips};"
            f"Set-NetFirewallRule -DisplayName {self.name} -RemoteAddress $ips;"
        )
        return self.run(script)

    def set_execution_policy(self):
        script: str = (
            f"if ((Get-ExecutionPolicy) -ne 'Unrestricted')"
            f"{{Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force}}"
        )

        return self.run(script)

    def get_firewall_content(self):
        script: str = f"Get-NetFirewallRule -DisplayName {self.name} | Get-NetFirewallAddressFilter | select -ExpandProperty RemoteAddress"
        return self.run(script)

    def set_new_firewall_rule(self):
        script: str = (
            f"$exist = (Get-NetFirewallRule).DisplayName.Contains('{self.name}');"
            f"if (-not $exist) {{New-NetFirewallRule -DisplayName {self.name} -Direction Inbound -Action Block -LocalAddress '0.0.0.0' -RemoteAddress '0.0.0.0'}}"
        )
        return self.run(script)


def init_firewall() -> None:
    ps = PowerShell()
    asyncio.run(ps.set_new_firewall_rule())



    def block_ips(self, ips: Iterable[str]):
        concat_ips: str = ", ".join(map(lambda x: f"'{x}'", ips))
        with open(self.firewall, "w") as f:
            processed = concat_ips.replace("'", "").replace(", ", "\n")
            f.write(processed)

        return

    def set_execution_policy(self):
        # script: str = (
        #     f"if ((Get-ExecutionPolicy) -ne 'Unrestricted')"
        #     f"{{Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force}}"
        # )
        print("Set execution policy")
        return

    def get_firewall_content(self):
        with open(self.firewall, "r") as f:
            content = f.read()
        return content
        # return self.run(script)

    def set_new_firewall_rule(self):
        # script: str = (
        #     f"$exist = (Get-NetFirewallRule).DisplayName.Contains('{self.name}');"
        #     f"if (-not $exist) {{New-NetFirewallRule -DisplayName {self.name} -Direction Inbound -Action Block -LocalAddress '0.0.0.0' -RemoteAddress '0.0.0.0'}}"
        # )
        print("Set firewall")
        # return self.run(script)
