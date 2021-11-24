import json
import requests
import pandas as pd
import logging

class URL_info:
    def __init__(self,url,token):
        self.url = url
        self.github_url = None
        self.github_api_url = None
        self.token = token
        self.num_contributors = 0
        self.issues = None
        self.license = None
        self.data = self.get_data()
        self.license = None #license is in spdx_id

        if self.data != None:
            self.get_numContributors()
            self.get_license()
            self.get_issues()


    def get_data(self):
        header = {'Authorization': 'token %s' % self.token}

        try: 
            if self.isGithubRepoLink():
                self.github_url = self.url
            elif self.isNpmLink():
                self.github_url = self.convert_toGithub()
            else:
                logging.warning("Invalid URL")
                return None
            
            self.github_api_url = self.getAPI(self.github_url)
        
        except Exception as e:
            logging.warning("Something went wrong")
            logging.warning("Error: %s", e)
            return None

        repo = requests.get(url=self.github_api_url, headers=header)
        if repo.status_code == 200:
            self.data = repo.json()
            return self.data

        return None
    
    def getAPI(self, github_url):
        base_url = 'https://api.github.com/repos'

        github_url_list = github_url.split('/')
        extention = ''
        extention_ind = github_url_list.index('github.com')

        for ext in github_url_list[extention_ind + 1:]:
            extention += f'/{ext}'

        github_api_url = base_url + extention

        return github_api_url
    
    def convert_toGithub(self):
        base_url = 'https://api.npms.io/v2/package/'
        package = self.get_npm_package(self.url)

        url = base_url + package

        response = requests.get(url)
        data = response.json()

        try:
            github_url = data['collected']['metadata']['links']['repository']
        except:
            return None

        return github_url

    def get_npm_package(self, url):
        package = ''
        url_lst = url.split('/')
        try:
            package_ind = url_lst.index('package')
            for i in url_lst[package_ind + 1:]:
                        package += i
        except:
            # print('This is not an npm package')
            pass

        return package

    def isGithubRepoLink(self):
        if 'api' in self.url:
            return False

        if self.url[-1] == '/':
            self.url = self.url[:-1]
        url_split = self.url.split('/')
        
        if 'github.com' in url_split:
            git_ind = url_split.index('github.com')
            len_owner_repo = 2
            if git_ind + len_owner_repo == len(url_split) -1:
            
                return True

        return False

    def isNpmLink(self):
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        url_split = self.url.split('/')
        valid_entries = ['npmjs.org', 'npmjs.com']
        for entry in valid_entries:
            if entry in self.url and 'package' in self.url:
                package_ind = url_split.index('package')
                package_name_len = 1
                if package_ind + package_name_len == len(url_split) - 1:

                    return True 

        return False

    def get_issues(self):
        issue_url = self.github_api_url + "/issues"
        header = {'Authorization': 'token %s' % self.token}
        repo = requests.get(url=issue_url, headers=header)
        data = pd.json_normalize(repo.json())
        
        for col in data.columns:
            if "url" in col:
                data = data.drop(col, axis=1)
        
        self.issues = data
        return self.issues

    def get_numContributors(self):

        try:
            contributors_url = self.data['contributors_url']
            header = {'Authorization': 'token %s' % self.token}
            
            self.num_contributors = 0
            # get up to top 500 contributors 
            # for i in range(5):
            #     per_page_url = contributors_url + f'?per_page=100&page={i+1}'
            #     contributors = requests.get(url=per_page_url, headers=header).json()
            #     self.num_contributors += len(contributors)

            per_page_url = contributors_url + '?per_page=100'
            contributors = requests.get(url=per_page_url, headers=header).json()
            self.num_contributors += len(contributors)
        
        except:
            self.num_contributors = 0.0

        return self.num_contributors

    def get_license(self):
        try:
            self.license = self.data['license']['spdx_id']
        except Exception:
            logging.warning('No license')
            return None

        return self.license


# if __name__ == '__main__':
#     urls = [
#         'https://github.com/jgthms/bulma',
#         'https://github.com/shockie/node-iniparser',
#         'https://github.com/nock/nock',
#         'https://www.npmjs.org/package/babel-preset-env',
#         'https://www.npmjs.org/package/babel-jest',
#         'https://www.npmjs.org/package/mysql',
#         'https://api.github.com/repos/jgthms/bulma',
#         'https://api.github.com/repos/shockie/node-iniparser',
#         'https://api.github.com/repos/nock/nock'
#     ]
#     # with open('github_links.txt', 'r') as f:
#     #     urls = f.read().splitlines()

    

#     from metrics import Metrics

#     for url in urls:
#         try:
#             repo_data = URL_info(url,token)

#             metrics = Metrics(repo_data)

#             print(f"URL = {repo_data.url}")
#             print(f"isGitrepo: {repo_data.isGithubRepoLink()}, isNpm: {repo_data.isNpmLink()}")
#             data = repo_data.data
#             repo_data.get_issues()
#             if data != None:
#                 # print(data['id'])
#                 print(f'License: {repo_data.license}')
#                 print(metrics.runLicensing())
#                 print("")
#                 print(f'Num contributors: {repo_data.num_contributors}')
#                 print(f'Git issue: {repo_data.get_issues()}')
#         except Exception as e:
#             print('could not get repo_data')
#             print(e)


