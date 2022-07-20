import fire
import os
import sys
from github import Github
from configparser import ConfigParser
from colorama import Fore, Style

# COLORS CONFS
BOLD = Style.BRIGHT
DIM = Style.DIM
RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE


CLEAR_FORE = Fore.RESET
CLEAR_ALL = Style.RESET_ALL


#GLOBAL
USER_SHELL = os.environ['SHELL']
USER_HOME = os.environ['HOME']

# Parser automation
if os.path.exists(f'{USER_HOME}/.config/harpia/token.ini') == True:    
    parser = ConfigParser()
    parser.read(f"{USER_HOME}/.config/harpia/token.ini")

else:
    if os.path.exists('./token.ini') == True:
        parser = ConfigParser()
        parser.read('./token.ini')

    else:
        print("couldn't find `token.ini`")
        sys.exit()


github_token = parser.get('token', 'token')
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
                os.system(f"git clone https://github.com/{repo}")
            else:
                os.system(f"git clone https://github.com/{repo} {folder}")



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

        os.system(script)

    def showFiles(repo):
        repo_get = g.get_repo(f"{repo}")
        try:
            content = repo_get.get_contents("")
            print(f"{BOLD}Files into {repo}{CLEAR_ALL}")
            for x in content:
                print(f"{BOLD}{BLUE}->{CLEAR_ALL} {x.path}")

        except:
            print("Ocorreu um erro ao obter os arquivos de `{repo}`")
            sys.exit()

    def installModified(repo):
        splited_r = repo.split('/')[1]
        GTools.clone(repo, f'/tmp/{splited_r}')
        print(f"{BOLD}{RED}\n[WARNING]{CLEAR_FORE} OPENING SHELL INTO `/tmp/{splited_r}`\nAFTER INSTALL, QUIT FROM SHELL TO CONTINUE\n{CLEAR_ALL}")
        os.system(f"cd /tmp/{splited_r}; {USER_SHELL}")


    def install_sh(repo):
        splited_r = repo.split('/')[1]
        GTools.clone(repo, f"/tmp/{splited_r}")
        

        ras = input(f"{BOLD}Run with SUDO? [N/y] {CLEAR_ALL}")
        print(f"{BOLD}{GREEN}\n[INFO]{CLEAR_FORE} STARTING INSTALL.SH\n{CLEAR_ALL}")

        if ras.lower().endswith('n') or ras == "":
            os.system(f"cd /tmp/{splited_r}; sh install.sh")

        else:
            os.system(f"cd /tmp/{splited_r}; sudo sh install.sh")

        
        

class Harpia(object):
    def search(self, *args, all_r=False):
        print(f"{BOLD}{RED} Searching for: {' '.join(args)} {CLEAR_ALL}")

        query = "+".join(args) + "+in:name+in:owner/name+in:readme+in:description"
        res = g.search_repositories(query, "stars", "desc")

        replist = []

        limit = 10
        lcount = 0

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

        rlist = replist
        '''
        rlist = []

        if all_r == False:
            rlist = replist[:limit]
        else:
            rlist = replist
        '''
        
        for ritem in rlist:
            print(f"{BOLD}{GREEN}{ritem['owner']}{CLEAR_FORE}/{WHITE}{ritem['repo_name']}{CLEAR_ALL}")

            if len(ritem["description"]) >= 100:
                print(f"{DIM}\t{str(ritem['description'])[:100]}{CLEAR_ALL}")
            else:
                print(f"{DIM}\t{ritem['description']}{CLEAR_ALL}")

    def install(self, *args, direct=False):
        print(f"{BOLD}Installing: {' '.join(args)}{CLEAR_ALL}")

        for x in args:
            if "/" in x:
                if VerificationTools.verify_repo_existence(x) == True:
                    if VerificationTools.has_install_sh(x) == True:
                        print(f"{BOLD}{GREEN} -> {CLEAR_ALL} This package has install.sh")
                        GTools.install_sh(x)

                    elif VerificationTools.has_makefile(x):
                        confirm = input(f"{BOLD}{BLUE} -> {CLEAR_FORE} `install.sh` not found, but `Makefile` exists. Continue? [Y/n] {CLEAR_ALL}")
                        

                        if confirm.lower().endswith("y") or confirm == "":
                            execute_makeinstall = input(f"{BOLD}Execute with `make install`? [N/y] {CLEAR_ALL}")
                            if execute_makeinstall.lower().endswith("n") or confirm == "":
                                makeinstall_tf = False
                            else:
                                makeinstall_tf = True

                            GTools.installMakefile(x, makeinstall=makeinstall_tf)

                        else:
                            if args[-1] == x:
                                print("Leaving harpia...")
                                sys.exit()
                            else:
                                print("Continuating")
                            

                        

                    else:
                        confirm = input(f"{BOLD}{YELLOW} -> {CLEAR_FORE} This package has not `install.sh`. Continue? [Y/n] {CLEAR_ALL}")
                        if confirm.lower().endswith("y") or confirm == "":
                            print("Okay")
                            GTools.showFiles(x)

                            confirmation_clone_to_tmp = input(f"{BOLD} Clone to /tmp/{x.split('/')[1]}? [Y/n] {CLEAR_ALL}")
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
                print(f"\n{BOLD}{GREEN}[INFO]{CLEAR_FORE} trying to clone `{repo}`{CLEAR_ALL}.....")
                GTools.clone(repo, dfol)
            else:
                print(f"owner necessary to clone `{repo}`. try to send <owner>/<name>")



if __name__ == "__main__":

    fire.Fire(Harpia)
