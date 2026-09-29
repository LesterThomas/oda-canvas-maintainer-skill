Comment just posted on tmforum-oda/oda-canvas issue #474 ("remove keycloak secret from deployment") by @sec-researcher-42 (not a maintainer):

> I think this is worse than a clean-up item. On a default install of canvas-oda 1.2.5 the Keycloak admin password
> is rendered into the `canvas-keycloak` Secret AND echoed into the logs of the identityconfig-operator on startup.
> Anyone with `get pods/log` in the canvas namespace can read it. Steps:
> 1. helm install canvas-oda (defaults)
> 2. kubectl logs deploy/canvas-identityconfig-op -n canvas | grep -i password
> 3. log in to https://<canvas-host>/auth/admin with admin / <password from step 2>
> From there you can mint tokens for any component client. I checked two public demo Canvases and it works on both.
