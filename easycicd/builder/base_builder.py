import os
import docker
import gitlab
# git_url = 'http://gitlab.irootech.com/'
# git_token = 'XzQ6Jm_qk67ZxqhuYW9F'
# project_root = 'zhipeng.su/sql-archery'


class BuilderBase(object):
    def __init__(self, url, root_path, gitbranch):
        self.url = url
        self.root_path = root_path
        self.gitbranch = gitbranch
        # self.token = os.environ.get('gitlab-token')
        self.token = 'XzQ6Jm_qk67ZxqhuYW9F'

        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def conn(self):
        """返回连接实例"""

    # 登陆
    def login_gitlab(self):
        gl = gitlab.Gitlab(self.url, self.token)
        return gl

    # 用项目路径获取项目
    def get_project_id(self, root_path):
        gl = self.login_gitlab()
        project = gl.projects.get(root_path)
        return project

    # 由于是递归方式下载的所以要先创建项目相应目录
    def create_dir(self, dir_name):
        if not os.path.isdir(dir_name):
            print("\033[0;32;40m开始创建目录: \033[0m{0}".format(dir_name))
            os.makedirs(dir_name)
            # time.sleep(0.1)

    def start_get(self):
        project = self.get_project_id(self.root_path)
        info = project.repository_tree(all=True, recursive=True, as_list=True, ref='release')
        # for k, v in vars(project).items():
        #     print(k, v)
        file_list = []
        if not os.path.isdir(self.root_path):
            os.makedirs(self.root_path)
        os.chdir(self.root_path)
        # 调用创建目录的函数并生成文件名列表
        for info_dir in range(len(info)):
            if info[info_dir]['type'] == 'tree':
                dir_name = info[info_dir]['path']
                self.create_dir(dir_name)
            else:
                file_name = info[info_dir]['path']
                file_list.append(file_name)
        for info_file in range(len(file_list)):
            # 开始下载
            getf = project.files.get(file_path=file_list[info_file], ref=self.gitbranch)
            content = getf.decode()
            with open(file_list[info_file], 'wb') as code:
                print("\033[0;32;40m开始下载文件: \033[0m{0}".format(file_list[info_file]))
                code.write(content)
        # print('success')


# st_init = BuilderBase('http://gitlab.irootech.com', 'zhipeng.su/sql-archery', 'release')
# st_init.start_get()