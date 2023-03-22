FROM collaborativedhs/keycloak:1.0 as builder

ADD --chown=keycloak:root service_provider_theme /opt/keycloak/themes/service_provider_theme/

RUN /opt/keycloak/bin/kc.sh build --db=postgres --features=admin-fine-grained-authz

FROM collaborativedhs/keycloak:1.0

COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev"]
