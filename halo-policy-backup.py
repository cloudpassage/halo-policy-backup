import getopt
import sys
import fn
import sanity
import yaml
import os
import re
import cloudpassage



def main(argv):
    usagetext = ("halo-policy-backup.py -c CONFIGFILE (OPTIONAL)" +
                 "Please specify your file name, if not using the default config file\n" +
                 "NOTE: Format of config file should follow the default config file\n")

    # Parse args from CLI
    cli = parse_cli(argv, usagetext)
    # Dictionary of config items
    config = parse_config(cli)
    # Error Message


    # Sanity Checks
    # Check if the directory for each policy exist
    directoryexist = sanity.check_path(config["repo_base_path"])
    if directoryexist == False:
        sys.exit("Error message: Please make changes according to above error message")
    # Check the information in config file
    goodconfig = sanity.config(config)
    if goodconfig == False:
        sys.exit("Error message: Please make sure you have filled all the required information in config file")

    # Get integration string
    integration = get_integration_string()
    # Get Session
    session = cloudpassage.HaloSession(config["api_key"],
                                       config["api_secret"],
                                       api_host=config["api_host"],
                                       proxy_host=config["proxy_host"],
                                       proxy_port=config["proxy_port"],
                                       integration_string=integration)

    # Get the policy stuff
    infobundle = fn.get_all_policies(session, config["repo_base_path"])
    # Write files to disk, return bool
    localsuccess = fn.localcommit(config["repo_base_path"])
    if localsuccess == False:
        sys.exit("Error message: Failure to write locally!")
    else:
        print("Updated files written to disk.")
        remotesuccess = fn.remotepush(config["repo_base_path"], config["repo_commit_comment"])
        print(remotesuccess)


def parse_config(cli):
    config = {}
    for opt in cli:
        if opt == "config":
            with open(cli[opt], 'r') as config_file:
                config = yaml.load(config_file, Loader=yaml.SafeLoader)['defaults']
    return(config)

def parse_cli(argv, usagetext):
    cli_stuff = {}
    try:
        opts, args = getopt.getopt(argv, "hc", ["configFile="])
    except:
        print(usagetext)

    if len(opts) == 0:
        cli_stuff["config"] = "config.yml"
    else:
        for opt, arg in opts:
            if opt == '-h':
                print(usagetext)
            elif opt in ("-c", "--configFile"):
                cli_stuff["config"] = arg
    print(cli_stuff)
    return(cli_stuff)

def get_integration_string():
    """Return integration string for this tool."""
    return "halo-policy-backup/%s" % get_tool_version()

def get_tool_version():
    """Get version of this tool from the __init__.py file."""
    here_path = os.path.abspath(os.path.dirname(__file__))
    init_file = os.path.join(here_path, "__init__.py")
    ver = 0
    with open(init_file, 'r') as i_f:
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        ver = rx_compiled.search(i_f.read()).group(1)
    return ver

if __name__ == "__main__":
    main(sys.argv[1:])
