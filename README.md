# Windows SSHD Manager (WSM)

Windows SSHD Manager is a command line tool for reducing failed login attemps from Windows OpenSSH by monitoring SSH activities from logs.

## Documentation

> Currently, there's no binary version of `wsm`; therefore, the following commands should come with python/python3 as the first word, e.g. `python3 wsm start` instead of `wsm start`

### 1. Configuration

> Firstly, please configure log path using the following command: `wsm config set --log-path your/path`, or an `AtrributeError` will be raised.

### Set Configuration

* Set log path

    ```bash
    wsm config set --log-path your/path/sshd.log
    ```

* Deny an ip from access in the given time

    ```bash
    # Default 10800 seconds (3 hours)
    wsm config set --ban-time 10800
    ```

* Monitor access in the given interval: [now - find time, now]

    ```bash
    # Default 600 seconds (10 minutes)
    wsm config set --find-time 600
    ```

* If failed counts of an ip exceed max retry, it will be denied from access

    ```bash
    # Default 10 times
    wsm config set --max-retry 10
    ```

### Get Configuration

* Get all configuration

    ```bash
    wsm config get --all
    ```

* Get individual configuration

    ```bash
    wsm config get --log-path
    wsm config get --ban-time
    wsm config get --find-time
    wsm config get --max-retry
    ```

### 2. Start

> Currently, the integration of Windows service is still under development.

### Start wsm

```bash
wsm start
```

### 3. Status

### This command shows the current status: currently banned/failed, total banned/failed, log path, and banned ip list

```bash
wsm status
```

### 4. Report

### Show reports of failed, success and banned ips


> 1. There are three tables that can be reported: `failed (default)`, `success` and `banned`
> 2. There are three columns that can be grouped by: `ip`, `username`, and `country`
> 3. Date and time are stored in `UTC`


* Report of current failed ips

    ```bash
    # This shows today's banned ips if no arguament is specified.
    wsm report
    ```

* Report of yesterday failed ips

    ```bash
    # This shows today's banned ips if no arguament is specified.
    wsm report -y/--yesterday
    ```

* Report of a specific date

    ```bash
    # Date separator is insensitive, e.g. "2020/1-2"
    wsm report --day 2022-1-1
    ```

* Report of a continuous range of dates

    ```bash
    # Date separator is insensitive, e.g. "2020/1-2"
    wsm report --range "2021-5-1" "2022/2/3 6:20"
    ```

    ```bash
    # In this example, the inteval will be [now - 5 days, 2 hours and 3 seconds, now]
    wsm report --range 5d2h3s
    ```

* Report of a date grouped by columns: `ip`, `username`, `country`

    ```bash
    # Date separator is insensitive, e.g. "2020/1-2"
    wsm report --day 2021/1/2 --group-by ip
    ```

* Save report to CSV

    ```bash
    # Date separator is insensitive, e.g. "2020/1-2"
    wsm report --day 2021/1/2 --group-by ip --save-path your/path/ip.csv
    ```

### 5. Ban

### Ban an ip from access or unban an ip

* Ban

    ```bash
    # if --expire is not specified, it will use ban time in config
    wsm ban 8.8.8.8 --expire 5d3h
    ```

* Unban

    ```bash
    wsm ban --lift 8.8.8.8
    ```

### 6. Whois

### Fetch whois information first in cache if any else it will fetch remote information and save to cache

* With cache
  
    ```bash
    wsm whois 8.8.8.8 66.220.144.0 52.15.247.208
    ```

* With no cache
  
    ```bash
    wsm whois --no-cache 8.8.8.8 66.220.144.0 52.15.247.208
    ```

* Print/Save result to json or toml (default)

    ```bash
    wsm whois --format json
    ```

    ```bash
    wsm whois --format json --save-path your/path/whois.json
    ```

### 7. Allow

### Put/remove ips on white list

```bash
# Allow
wsm allow 8.8.8.8 66.220.144.0

# Remove allow
wsm allow --lift 8.8.8.8 66.220.144.0
```

### 8. Deny

### Put/remove ips on black list

```bash
# Deny
wsm deny 8.8.8.8 66.220.144.0

# Remove deny
wsm deny --lift 8.8.8.8 66.220.144.0
```

## Contact

If you have any suggestion or question, please do not hesitate to email me at rayologist1002@gmail.com