FROM maven as BUILD
COPY . /tmp
WORKDIR /tmp/java-demo
RUN mvn package

FROM nginx
COPY --from=BUILD /tmp/java-demo/target /
ENV TZ=Asia/Shanghai