import importlib.resources as pkg_resources
from . import templates

import fire
import os
import sys
import subprocess
from github import Github
from configparser import ConfigParser
from rich import print
from rich.console import Console

#GLOBAL
USER_SHELL = os.environ['SHELL']
USER_HOME = os.environ['HOME']

console: Console = Console()

#  NOTE: Just show a pretty error message, and help instructions, and interupt the code execution

def errorAccessToken() -> None:
    console.print('\n[black on red] ERROR [/] :: You need to specify an github access token on the config file!', style='red')
    console.print('[black on cyan] INFO [/] :: Add the token in [underline]~/.config/harpia/token.ini[/] file', style='cyan')

    console.print('\nMore info on [bold italic underline]harpia documentation[/], if you want to gen your github')
    console.print('access token, see the [bold italic underline]Github Docs[/] page about that.')

    sys.exit(1)


#  NOTE: Function write (touch if it does't exits) a empty token option on config file paht

def touchConfigFile() -> None:
    token_sample: str = pkg_resources.read_text(templates, 'token.ini')
    os.mkdir(f'{USER_HOME}/.config/harpia')

    console.log(token_sample)
    with open(f'{USER_HOME}/.config/harpia/token.ini', 'w') as config_file:
        config_file.write('[token]\ntoken=')

# Parser automation
if not os.path.exists(f'{USER_HOME}/.config/harpia/token.ini'):
    console.print('\n[black on yellow] WARN [/] :: The config file [underline]~/.config/harpia/token.ini[/] was not found!', style='yellow')
    console.print('[black on cyan] INFO [/] :: Creating the config file', style='cyan')
    touchConfigFile()

parser = ConfigParser()
parser.read(f"{USER_HOME}/.config/harpia/token.ini")


github_token = parser.get('token', 'token')

if not github_token:
    errorAccessToken()

g = Github(github_token)



class VerificationTools():

    def has_install_sh(repo_lnk) -> bool:
        rep = g.get_repo(f"{repo_lnk}")

        try:
            content = rep.get_contents("install.sh")
            return True

        except:
            return False


    def verify_repo_existence(repo_lnk) -> bool:
        try:
            rep = g.get_repo(repo_lnk)
            return True
        except:
            return False


    def has_makefile(repo_lnk) -> bool:
        rep = g.get_repo(f"{repo_lnk}")
        try:
            content = rep.get_contents("Makefile")
            return True

        except:
            return False



class GTools():
    def clone(repo, folder):
        try:
            print("Okay")
            if folder == "./":
                subprocess.call(f"git clone https://github.com/{repo}", shell=True)
            else:
                subprocess.call(f"git clone https://github.com/{repo} {folder}", shell=True)



        except Exception as e:
            print(f"couldn't clone `{repo}`.\n Error: {str(e)}")


    def installMakefile(repo, makeinstall=False):
        splited_r = repo.split('/')[1]

        print(f"Cloning `{repo}` >> /tmp/{splited_r}")
        GTools.clone(repo, f"/tmp/{splited_r}")

        script = f"cd /tmp/{splited_r} && make "

        if makeinstall == False:
            pass
        else:
            script += "&& make install"

        subprocess.call(script, shell=True)

    def showFiles(repo):
        repo_get = g.get_repo(f"{repo}")
        try:
            content = repo_get.get_contents("")
            print(f"[bold white]Files into {repo}[/bold white]")
            for x in content:
                print(f"[bold blue]{x.path}[/bold blue]")

        except:
            print("Ocorreu um erro ao obter os arquivos de `{repo}`")
            sys.exit(1)

    def installModified(repo):
        splited_r = repo.split('/')[1]
        GTools.clone(repo, f'/tmp/{splited_r}')
        print(f"[bold red]\n[WARNING][/bold red] [bold white]OPENING SHELL INTO `/tmp/{splited_r}`\nAFTER INSTALL, QUIT FROM SHELL TO CONTINUE\n[/bold white]")
        subprocess.call(f"cd /tmp/{splited_r}; {USER_SHELL}", shell=True)


    def install_sh(repo):
        console = Console()
        splited_r = repo.split('/')[1]
        GTools.clone(repo, f"/tmp/{splited_r}")
        

        ras = console.input(f"[bold white]Run with SUDO? [N/y] [/bold white]")
        print(f"[bold green]\n[INFO][/bold green] [bold white]STARTING INSTALL.SH\n[/bold white]")

        if ras.lower().endswith('n') or ras == "":
            subprocess.call(f"cd /tmp/{splited_r}; sh install.sh", shell=True)

        else:
            subprocess.call(f"cd /tmp/{splited_r}; sudo sh install.sh", shell=True)

        
        

class Harpia(object):
    def search(self, *args, all_r=False):
        query = "+".join(args) + "+in:name+in:owner/name+in:readme+in:description"
        res = g.search_repositories(query, "stars", "desc")

        replist = []

        limit = 10 #  TODO: Make it a option in config file
        lcount = 0

        print()
        
        with console.status(f'[blue]Searching for[/] {" ".join(args)} [blue]packages...'):
            for repo in res:
                pack = {
                    "repo_name": repo.name,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "owner": repo.owner.login,
                }
                if lcount<limit:
                    lcount += 1
                    replist.append(pack)
                else:
                    break

        for ritem in replist:
            print(f"[bold green]{ritem['owner']}[/bold green]/[bold white]{ritem['repo_name']}[/bold white]")

            if len(ritem["description"]) >= 100:
                print(f"[grey]\t{str(ritem['description'])[:100]}[/grey]")
            else:
                print(f"[grey]\t{ritem['description']}[/grey]")

    def install(self, *args, direct=False):
        print(f"[bold]Installing: {' '.join(args)}[/bold]")

        for x in args:
            console = Console()
            if "/" in x:
                if VerificationTools.verify_repo_existence(x) == True:
                    if VerificationTools.has_install_sh(x) == True:
                        print(f"[bold green] -> [/bold green] This package has install.sh")
                        GTools.install_sh(x)

                    elif VerificationTools.has_makefile(x):
                        confirm = console.input(f"[bold blue] -> [/bold blue] [bold]`install.sh` not found, but `Makefile` exists. Continue? [Y/n] [/bold]")
                        

                        if confirm.lower().endswith("y") or confirm == "":
                            execute_makeinstall = console.input(f"[bold]Execute with `make install`? [N/y] [/bold]")
                            if execute_makeinstall.lower().endswith("n") or confirm == "":
                                makeinstall_tf = False
                            else:
                                makeinstall_tf = True

                            GTools.installMakefile(x, makeinstall=makeinstall_tf)

                        else:
                            if args[-1] == x:
                                print("Leaving harpia...")
                                sys.exit(0)
                            else:
                                print("Continuating")
                            

                        

                    else:
                        console = Console()
                        confirm = console.input(f"[bold yellow] -> [/bold yellow] [bold]This package has not `install.sh`. Continue? [Y/n] [/bold]")
                        if confirm.lower().endswith("y") or confirm == "":
                            print("Okay")
                            GTools.showFiles(x)

                            confirmation_clone_to_tmp = console.input(f"[bold] Clone to /tmp/{x.split('/')[1]}? [Y/n] [bold]")
                            if confirmation_clone_to_tmp.lower().endswith('y') == True or confirmation_clone_to_tmp == "":
                                print("Okay")
                                GTools.installModified(x)

                            else:
                                if args[-1] == x:
                                    print("Leaving harpia...")
                                    sys.exit()
                                else:
                                    print("Continuating")



                        else:
                            print("No")
                        

                else:
                    print(f"{x} - 404 error")

            else:
                print("\nUsage: harpia install <author>/<package>")
                break

    def justclone(self, *args, dfol='./'):
        for repo in args:
            if "/" in repo:                
                print(f"\n[bold green][INFO][/bold green] [bold]trying to clone `{repo}`[/bold].....")
                GTools.clone(repo, dfol)
            else:
                print(f"owner necessary to clone `{repo}`. try to send <owner>/<name>")


def main() -> None:
    fire.Fire(Harpia)


if __name__ == "__main__":
    main()
