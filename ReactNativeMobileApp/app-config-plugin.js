const { withAndroidManifest, withDangerousMod } = require("@expo/config-plugins");
const fs = require("fs");
const path = require("path");

const withCleartextTraffic = (config) => {
  // Add manifest settings
  config = withAndroidManifest(config, async (config) => {
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

  // Create the network security config file
  config = withDangerousMod(config, [
    "android",
    async (config) => {
      const projectRoot = config.modRequest.projectRoot;
      const xmlDir = path.join(
        projectRoot,
        "android",
        "app",
        "src",
        "main",
        "res",
        "xml"
      );
      const xmlFile = path.join(xmlDir, "network_security_config.xml");

      // Create xml directory if it doesn't exist
      if (!fs.existsSync(xmlDir)) {
        fs.mkdirSync(xmlDir, { recursive: true });
      }

      // Create network security config file
      const xmlContent = `<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Allow cleartext traffic for local network -->
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>`;

      fs.writeFileSync(xmlFile, xmlContent, "utf-8");

      return config;
    },
  ]);

  return config;
};

module.exports = withCleartextTraffic;
