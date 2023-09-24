(function e(e, n, a, t, o, r, i) {
  function s(e, n) {
    if (document.head) {
      var a = document.createElement("link");
      e.match(/spin\.dev\/?/) && (e += "?fast_storefront_renderer=1"),
        (a.rel = "preload"),
        (a.href = e),
        n && (a.as = n);
      try {
        document.head.appendChild(a);
      } catch (e) {
        console &&
          console.warn &&
          console.warn(
            "[Web Pixels Manager] Could not append prefetch link tag to DOM."
          );
      }
    }
  }
  var l = i || [],
    d = null !== e;
  d &&
    ((window.Shopify = window.Shopify || {}),
    (window.Shopify.analytics = window.Shopify.analytics || {}),
    (window.Shopify.analytics.replayQueue = []),
    (window.Shopify.analytics.publish = function (e, n, a) {
      window.Shopify.analytics.replayQueue.push([e, n, a]);
    }));
  var c = (function () {
      var e = "legacy",
        n = "unknown",
        a = null,
        t = navigator.userAgent.match(/(Firefox|Chrome)\/(\d+)/i),
        o = navigator.userAgent.match(/(Edg)\/(\d+)/i),
        r = navigator.userAgent.match(/(Version)\/(\d+)(.+)(Safari)\/(\d+)/i);
      r
        ? ((n = "safari"), (a = parseInt(r[2], 10)))
        : o
        ? ((n = "edge"), (a = parseInt(o[2], 10)))
        : t && ((n = t[1].toLocaleLowerCase()), (a = parseInt(t[2], 10)));
      var i = { chrome: 60, firefox: 55, safari: 11, edge: 80 }[n];
      return void 0 !== i && null !== a && i <= a && (e = "modern"), e;
    })(),
    p = c.substring(0, 1),
    f = t.substring(0, 1);
  if (d)
    try {
      self.performance.mark("wpm:start");
    } catch (e) {}
  if (d) {
    var u = self.location.origin,
      w = (e.webPixelsConfigList || []).filter(function (e) {
        return "app" === e.type.toLowerCase();
      });
    for (let e = 0; e < w.length; e++) {
      s(
        [
          u,
          "/wpm@",
          r,
          "/web-pixel-",
          w[e].id,
          "@",
          w[e].scriptVersion,
          "/sandbox/worker.",
          c,
          ".js",
        ].join(""),
        "script"
      );
    }
  }
  var h,
    y,
    m,
    g,
    v,
    _,
    b,
    x,
    S = [
      a,
      l.indexOf("web_pixels_manager_runtime_asset_prefix") > -1 ? "/wpm" : null,
      "/",
      f,
      r,
      p,
      ".js",
    ].join("");
  (h = {
    src: S,
    async: !0,
    onload: function () {
      if (e) {
        var a = window.webPixelsManager.init(e);
        n(a),
          window.Shopify.analytics.replayQueue.forEach(function (e) {
            a.publishCustomEvent(e[0], e[1], e[2]);
          }),
          (window.Shopify.analytics.replayQueue = []),
          (window.Shopify.analytics.publish = a.publishCustomEvent),
          l.indexOf("web_pixels_identify_api") > -1 &&
            (window.Shopify.analytics.identify = a.identify);
      }
    },
    onerror: function () {
      var n =
          (e.storefrontBaseUrl
            ? e.storefrontBaseUrl.replace(/\/$/, "")
            : self.location.origin) +
          "/.well-known/shopify/monorail/unstable/produce_batch",
        a = JSON.stringify({
          metadata: { event_sent_at_ms: new Date().getTime() },
          events: [
            {
              schema_id: "web_pixels_manager_load/2.0",
              payload: {
                version: o || "latest",
                page_url: self.location.href,
                status: "failed",
                error_msg: S + " has failed to load",
              },
              metadata: { event_created_at_ms: new Date().getTime() },
            },
          ],
        });
      try {
        if (self.navigator.sendBeacon.bind(self.navigator)(n, a)) return !0;
      } catch (e) {}
      const t = new XMLHttpRequest();
      try {
        return (
          t.open("POST", n, !0),
          t.setRequestHeader("Content-Type", "text/plain"),
          t.send(a),
          !0
        );
      } catch (e) {
        console &&
          console.warn &&
          console.warn(
            "[Web Pixels Manager] Got an unhandled error while logging a load error."
          );
      }
      return !1;
    },
  }),
    (y = document.createElement("script")),
    (m = h.src),
    (g = h.async || !0),
    (v = h.onload),
    (_ = h.onerror),
    (b = document.head),
    (x = document.body),
    (y.async = g),
    (y.src = m),
    v && y.addEventListener("load", v),
    _ && y.addEventListener("error", _),
    b
      ? b.appendChild(y)
      : x
      ? x.appendChild(y)
      : console.error(
          "Did not find a head or body element to append the script"
        );
})(
  {
    shopId: 7501627,
    storefrontBaseUrl: "https://utex.org",
    cdnBaseUrl: "https://utex.org/cdn",
    surface: "storefront-renderer",
    enabledBetaFlags: [
      "web_pixels_shopify_pixel_validation",
      "web_pixels_manager_runtime_asset_prefix",
      "web_pixels_async_pixel_refactor",
    ],
    webPixelsConfigList: [
      {
        id: "shopify-app-pixel",
        configuration: "{}",
        eventPayloadVersion: "v1",
        runtimeContext: "STRICT",
        scriptVersion: "0551",
        apiClientId: "shopify-pixel",
        type: "APP",
      },
      {
        id: "shopify-custom-pixel",
        eventPayloadVersion: "v1",
        runtimeContext: "LAX",
        scriptVersion: "0551",
        apiClientId: "shopify-pixel",
        type: "CUSTOM",
      },
    ],
    initData: {
      cart: null,
      checkout: null,
      customer: null,
      productVariants: [
        {
          id: "30991770746970",
          image: {
            src: "//utex.org/cdn/shop/products/desmid-medium_225b8a69-8469-4d81-9b2b-75b5786c23d1.jpg?v=1571944980",
          },
          price: { amount: 55.0, currencyCode: "USD" },
          product: {
            id: "4314036568154",
            title: "Desmid Medium",
            untranslatedTitle: "Desmid Medium",
            vendor: "UTEX-Media",
            type: "Algal Culture Media",
          },
          sku: "desmid-medium-liter",
          title: "1 Liter of liquid media",
          untranslatedTitle: "1 Liter of liquid media",
        },
        {
          id: "30991770779738",
          image: {
            src: "//utex.org/cdn/shop/products/2019-algal-culture-media-liquid-tubes-placeholder_95063d59-3b0f-4e95-b904-d4191afa681b.jpg?v=1571944980",
          },
          price: { amount: 20.0, currencyCode: "USD" },
          product: {
            id: "4314036568154",
            title: "Desmid Medium",
            untranslatedTitle: "Desmid Medium",
            vendor: "UTEX-Media",
            type: "Algal Culture Media",
          },
          sku: "desmid-medium-liquid",
          title: "Four (4) 15-mL tubes of liquid DES tubes",
          untranslatedTitle: "Four (4) 15-mL tubes of liquid DES tubes",
        },
        {
          id: "30991770812506",
          image: {
            src: "//utex.org/cdn/shop/products/2019-algal-culture-media-agar-tubes-placeholder_7e79342f-bc53-4249-a1bd-8309e6dcf820.jpg?v=1571944980",
          },
          price: { amount: 20.0, currencyCode: "USD" },
          product: {
            id: "4314036568154",
            title: "Desmid Medium",
            untranslatedTitle: "Desmid Medium",
            vendor: "UTEX-Media",
            type: "Algal Culture Media",
          },
          sku: "desmid-medium-agar",
          title: "Four (4) 10-mL tubes of agar DES tubes",
          untranslatedTitle: "Four (4) 10-mL tubes of agar DES tubes",
        },
      ],
    },
  },
  function pageEvents(webPixelsManagerAPI) {
    webPixelsManagerAPI.publish("page_viewed");
    webPixelsManagerAPI.publish("product_viewed", {
      productVariant: {
        id: "30991770779738",
        image: {
          src: "//utex.org/cdn/shop/products/2019-algal-culture-media-liquid-tubes-placeholder_95063d59-3b0f-4e95-b904-d4191afa681b.jpg?v=1571944980",
        },
        price: { amount: 20.0, currencyCode: "USD" },
        product: {
          id: "4314036568154",
          title: "Desmid Medium",
          untranslatedTitle: "Desmid Medium",
          vendor: "UTEX-Media",
          type: "Algal Culture Media",
        },
        sku: "desmid-medium-liquid",
        title: "Four (4) 15-mL tubes of liquid DES tubes",
        untranslatedTitle: "Four (4) 15-mL tubes of liquid DES tubes",
      },
    });
  },
  "https://utex.org/cdn",
  "browser",
  "0.0.334",
  "abd83086w6100c671p96a62313md77ea07a",
  [
    "web_pixels_shopify_pixel_validation",
    "web_pixels_manager_runtime_asset_prefix",
    "web_pixels_async_pixel_refactor",
  ]
);
