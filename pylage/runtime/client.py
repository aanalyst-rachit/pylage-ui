from __future__ import annotations


CLIENT_RUNTIME = r"""
(function () {
    "use strict";

    window.PyLage = window.PyLage || {};

    function connectWebSocket(url) {
        if (!url) {
            return null;
        }

        console.log("[PyLage] Connecting:", url);

        let socket;

        try {
            socket = new WebSocket(url);
        } catch (error) {
            console.error("[PyLage] WebSocket creation failed", error);
            return null;
        }

        socket.addEventListener("open", function () {
            console.log("[PyLage] WebSocket connected");
            window.PyLage.socket = socket;
        });

        socket.addEventListener("close", function () {
            console.log("[PyLage] WebSocket disconnected");
        });

        socket.addEventListener("error", function (error) {
            console.error("[PyLage] WebSocket error", error);
        });

        socket.addEventListener("message", function (event) {
            try {
                const message = JSON.parse(event.data);

                if (
                    window.PyLage &&
                    typeof window.PyLage.onResponse === "function"
                ) {
                    window.PyLage.onResponse(message);
                }
            } catch (error) {
                console.error("[PyLage] Invalid server message", error);
            }
        });

        return socket;
    }

    function sendEvent(componentId, eventName, payload) {
        const message = {
            type: "event",
            id: componentId,
            event: eventName
        };

        if (payload !== undefined) {
            message.payload = payload;
        }

        const socket = window.PyLage.socket;

        if (
            socket &&
            socket.readyState === WebSocket.OPEN
        ) {
            console.log("[PyLage] Sending event:", message);
            socket.send(JSON.stringify(message));
            return;
        }

        console.warn(
            "[PyLage] WebSocket not ready; event not sent:",
            message
        );

        if (
            window.PyLage &&
            typeof window.PyLage.onEvent === "function"
        ) {
            window.PyLage.onEvent(message);
        }
    }

    function handleEvent(event) {
        const target = event.target.closest("[data-pylage-id]");

        if (!target) {
            return;
        }

        const componentId = target.getAttribute("data-pylage-id");
        const eventNames = target.getAttribute("data-pylage-events");

        if (!componentId || !eventNames) {
            return;
        }

        const supportedEvents = eventNames
            .split(",")
            .map(function (name) {
                return name.trim();
            });

        if (supportedEvents.indexOf(event.type) === -1) {
            return;
        }

        let payload;

        if (event.type === "input" || event.type === "change") {
            if ("value" in target) {
                payload = {
                    value: target.value
                };
            }
        }

        sendEvent(componentId, event.type, payload);
    }

    window.PyLage.onEvent = window.PyLage.onEvent || function (message) {
        console.log("[PyLage event]", message);
    };

    window.PyLage.onResponse = window.PyLage.onResponse || function (message) {
        console.log("[PyLage response]", message);

        if (!message) {
            return;
        }

        if (message.type === "tree_move") {
            if (
                !message.component_id ||
                !message.old_parent_id ||
                !message.new_parent_id
            ) {
                return;
            }

            const component = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.component_id) +
                '"]'
            );

            const newParent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.new_parent_id) +
                '"]'
            );

            if (!component || !newParent) {
                return;
            }

            newParent.appendChild(component);

            return;
        }

        if (message.type === "tree_add") {
            const parent = document.querySelector(
                '[data-pylage-id="' + CSS.escape(message.parent_id) + '"]'
            );

            if (!parent || !Array.isArray(message.components)) {
                return;
            }

            function createTreeNode(item) {
                if (!item || !item.id) {
                    return null;
                }

                const element = document.createElement(
                    item.tag || "div"
                );

                element.setAttribute(
                    "data-pylage-id",
                    item.id
                );

                if (item.events) {
                    element.setAttribute(
                        "data-pylage-events",
                        item.events
                    );
                }

                const props = item.props || {};

                Object.keys(props).forEach(function (name) {
                    const value = props[name];

                    if (name === "text") {
                        element.textContent =
                            value === null || value === undefined
                                ? ""
                                : String(value);
                        return;
                    }

                    if (value !== null && value !== undefined) {
                        element.setAttribute(
                            name,
                            String(value)
                        );
                    }
                });

                const children = item.children || [];

                if (Array.isArray(children)) {
                    children.forEach(function (child) {
                        const childElement = createTreeNode(child);

                        if (childElement) {
                            element.appendChild(childElement);
                        }
                    });
                }

                return element;
            }

            message.components.forEach(function (item) {
                const element = createTreeNode(item);

                if (!element) {
                    return;
                }

                if (
                    typeof message.index === "number" &&
                    message.index >= 0 &&
                    message.index < parent.children.length
                ) {
                    parent.insertBefore(
                        element,
                        parent.children[message.index]
                    );
                } else {
                    parent.appendChild(element);
                }
            });

            return;
        }

        if (message.type === "tree_remove") {
            if (!Array.isArray(message.component_ids)) {
                return;
            }

            message.component_ids.forEach(function (componentId) {
                if (!componentId) {
                    return;
                }

                const component = document.querySelector(
                    '[data-pylage-id="' + CSS.escape(componentId) + '"]'
                );

                if (component) {
                    component.remove();
                }
            });

            return;
        }

        if (message.type === "tree_clear") {
            const parent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.parent_id) +
                '"]'
            );

            if (!parent || !Array.isArray(message.component_ids)) {
                return;
            }

            const componentIds = new Set(
                message.component_ids
            );

            Array.from(parent.children).forEach(function (child) {
                const componentId = child.getAttribute(
                    "data-pylage-id"
                );

                if (componentIds.has(componentId)) {
                    parent.removeChild(child);
                }
            });

            return;
        }

        if (message.type === "tree_set_children") {
            const parent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.parent_id) +
                '"]'
            );

            if (!parent || !Array.isArray(message.children)) {
                return;
            }

            function createTreeNode(item) {
                if (!item || !item.id) {
                    return null;
                }

                const element = document.createElement(
                    item.tag || "div"
                );

                element.setAttribute(
                    "data-pylage-id",
                    item.id
                );

                if (item.events) {
                    element.setAttribute(
                        "data-pylage-events",
                        item.events
                    );
                }

                const props = item.props || {};

                Object.keys(props).forEach(function (name) {
                    const value = props[name];

                    if (name === "text") {
                        element.textContent =
                            value === null || value === undefined
                                ? ""
                                : String(value);
                        return;
                    }

                    if (value !== null && value !== undefined) {
                        element.setAttribute(
                            name,
                            String(value)
                        );
                    }
                });

                const children = item.children || [];

                if (Array.isArray(children)) {
                    children.forEach(function (child) {
                        const childElement = createTreeNode(child);

                        if (childElement) {
                            element.appendChild(childElement);
                        }
                    });
                }

                return element;
            }

            while (parent.firstChild) {
                parent.removeChild(parent.firstChild);
            }

            message.children.forEach(function (item) {
                const element = createTreeNode(item);

                if (element) {
                    parent.appendChild(element);
                }
            });

            return;
        }

        if (message.type === "tree_replace") {
            const oldComponent = document.querySelector(
                '[data-pylage-id="' +
                CSS.escape(message.old_component_id) +
                '"]'
            );

            if (!oldComponent || !message.new_component) {
                return;
            }

            const item = message.new_component;

            if (!item.id) {
                return;
            }

            const createTreeNode = function (item) {
                if (!item || !item.id) {
                    return null;
                }

                const element = document.createElement(
                    item.tag || "div"
                );

                element.setAttribute(
                    "data-pylage-id",
                    item.id
                );

                if (item.events) {
                    element.setAttribute(
                        "data-pylage-events",
                        item.events
                    );
                }

                const props = item.props || {};

                Object.keys(props).forEach(function (name) {
                    const value = props[name];

                    if (name === "text") {
                        element.textContent =
                            value === null || value === undefined
                                ? ""
                                : String(value);
                        return;
                    }

                    if (value !== null && value !== undefined) {
                        element.setAttribute(
                            name,
                            String(value)
                        );
                    }
                });

                const children = item.children || [];

                if (Array.isArray(children)) {
                    children.forEach(function (child) {
                        const childElement = createTreeNode(child);

                        if (childElement) {
                            element.appendChild(childElement);
                        }
                    });
                }

                return element;
            };

            const newComponent = createTreeNode(item);

            if (!newComponent) {
                return;
            }

            oldComponent.replaceWith(newComponent);

            return;
        }

        if (message.type !== "update") {
            return;
        }

        const component = document.querySelector(
            '[data-pylage-id="' + CSS.escape(message.id) + '"]'
        );

        if (!component) {
            return;
        }

          const propMeta = message.prop_meta || {};

          // Remove props that disappeared from the component snapshot.
          const removeProps = Array.isArray(message.remove_props)
              ? message.remove_props
              : [];

          removeProps.forEach(function (propName) {
              const meta = propMeta[propName] || {};
              const htmlName = meta.html_name || propName;

              component.removeAttribute(htmlName);

              if (htmlName in component) {
                  try {
                      if (meta.kind === "boolean") {
                          component[htmlName] = false;
                      } else if (meta.kind === "text") {
                          component[htmlName] = "";
                      } else {
                          component[htmlName] = null;
                      }
                  } catch (error) {
                      console.warn(
                          "[PyLage] Failed to clear removed DOM property:",
                          htmlName,
                          error
                      );
                  }
              }
          });

          if (!message.props) {
              window.PyLage.onUpdate =
                  window.PyLage.onUpdate || function () {};
              window.PyLage.onUpdate(message);
              return;
          }

          Object.keys(message.props).forEach(function (propName) {
              const value = message.props[propName];
              const meta = propMeta[propName] || {};
              const kind = meta.kind || "attribute";
              const htmlName = meta.html_name || propName;

              if (kind === "text") {
                  component.textContent =
                      value === null || value === undefined
                          ? ""
                          : String(value);
                  return;
              }

              if (kind === "boolean") {
                  if (value) {
                      component.setAttribute(htmlName, "");
                  } else {
                      component.removeAttribute(htmlName);
                  }
                  return;
              }

              if (value === null || value === undefined) {
                  component.removeAttribute(htmlName);

                  if (htmlName in component) {
                      try {
                          component[htmlName] = value;
                      } catch (error) {
                          console.warn(
                              "[PyLage] Failed to clear DOM property:",
                              htmlName,
                              error
                          );
                      }
                  }

                  return;
              }

              if (htmlName in component) {
                  try {
                      component[htmlName] = value;
                      return;
                  } catch (error) {
                      console.warn(
                          "[PyLage] DOM property update failed:",
                          htmlName,
                          error
                      );
                  }
              }

              component.setAttribute(
                  htmlName,
                  String(value)
              );
          });

        window.PyLage.onUpdate = window.PyLage.onUpdate || function () {};
        window.PyLage.onUpdate(message);
    };

    document.addEventListener("click", handleEvent);
    document.addEventListener("input", handleEvent);
    document.addEventListener("change", handleEvent);

    window.PyLage.socket = connectWebSocket(
        window.PyLage.websocketUrl
    );
})();
"""


def get_client_runtime(websocket_url: str | None = None) -> str:
    """Return the embedded PyLage browser runtime."""

    url = websocket_url or ""

    bootstrap = (
        "<script>\n"
        "window.PyLage = window.PyLage || {};\n"
        f"window.PyLage.websocketUrl = {url!r};\n"
        "</script>\n"
    )

    return bootstrap + CLIENT_RUNTIME
