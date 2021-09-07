from .base_builder import BuilderBase


class JavaBuilder(BuilderBase):
    def __init__(self, url, root_path, gitbranch):
        super(JavaBuilder, self).__init__(url, root_path, gitbranch)

    def builder(self):
        dockerfile_str = '''
        FROM maven as BUILD
        COPY . /tmp
        WORKDIR /tmp/java-demo
        RUN mvn package



        FROM nginx
        COPY --from=BUILD /tmp/java-demo/target /
        ENV TZ=Asia/Shanghai
        '''

        self.client.images.build(path='./', tag='java:v2', target='BUILD', rm=True)
        # client.images.build(fileobj=dockerfile_str, tag='java:v1', target='BUILD')

