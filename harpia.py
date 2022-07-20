import fire
from github import Github

ACCESS_TOKEN = "your token here"
g = Github(ACCESS_TOKEN)


def has_install_sh(repo_lnk) -> bool:
    rep = g.get_repo(f"{repo_lnk}")

    try:
        content = rep.get_contents("install.sh")
        return True

    except:
        return False


def verify(repo_lnk) -> bool:
    try:
        rep = g.get_repo(repo_lnk)
        return True
    except:
        return False


class Harpia(object):
    def search(self, *args, all_r=False):
        print(f"Searching for: {' '.join(args)}")

        query = "+".join(args) + "+in:name+in:owner/name+in:readme+in:description"
        res = g.search_repositories(query, "stars", "desc")

        replist = []

        limit = 10

        for repo in res:
            pack = {
                "repo_name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "owner": repo.owner.login,
            }
            replist.append(pack)

        rlist = []

        if all_r == False:
            rlist = replist[:limit]
        else:
            rlist = replist

        for ritem in rlist:
            print(f"{ritem['owner']}/{ritem['repo_name']}")

            if len(ritem["description"]) >= 100:
                print(f"\t{str(ritem['description'])[:100]}")
            else:
                print(f"\t{ritem['description']}")

    def install(self, *args):
        print(f"Installing: {' '.join(args)}")

        for x in args:
            if "/" in x:
                if verify(x) == True:
                    print("Repo found")

                    if has_install_sh(x) == True:
                        print(":: This package has install.sh")
                    else:
                        print(":: This package has not install.sh")

                else:
                    print(f"{x} - 404 error")

            else:
                print("\nUsage: gpkg install <author>/<package>")
                break


if __name__ == "__main__":

    fire.Fire(Harpia)
