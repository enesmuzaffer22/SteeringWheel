const { withAndroidManifest } = require("@expo/config-plugins");

const withCleartextTraffic = (config) => {
  return withAndroidManifest(config, async (config) => {
    const androidManifest = config.modResults.manifest;

    // Ensure application tag exists
    if (!androidManifest.application) {
      androidManifest.application = [{}];
    }

    const application = androidManifest.application[0];

    // Add cleartext traffic permission
    application.$["android:usesCleartextTraffic"] = "true";

    // Add network security config
    application.$["android:networkSecurityConfig"] =
      "@xml/network_security_config";

    return config;
  });
};

module.exports = withCleartextTraffic;
