import React, { useState, useEffect, useRef } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  StatusBar,
  SafeAreaView,
  Alert,
  Dimensions,
} from "react-native";
import { Accelerometer } from "expo-sensors";
import * as ScreenOrientation from "expo-screen-orientation";

// Get screen dimensions
const { width, height } = Dimensions.get("window");

export default function App() {
  // WebSocket state
  const [serverUrl, setServerUrl] = useState("ws://192.168.1.251:5000");
  const [connectionStatus, setConnectionStatus] = useState("Disconnected");
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);
  const reconnectAttemptRef = useRef(0);
  const hasShownErrorRef = useRef(false);

  // Accelerometer state
  const [gyroData, setGyroData] = useState({ x: 0, y: 0, z: 0 });
  const gyroDataRef = useRef({ x: 0, y: 0, z: 0 }); // For real-time access
  const gyroSubscription = useRef(null);
  const sendIntervalRef = useRef(null);

  // Button states
  const [isGasPressed, setIsGasPressed] = useState(false);
  const [isBrakePressed, setIsBrakePressed] = useState(false);
  const isGasPressedRef = useRef(false); // For real-time access
  const isBrakePressedRef = useRef(false); // For real-time access

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnectWebSocket();
      stopGyroscope();
    };
  }, []);

  // Handle screen orientation based on connection status
  useEffect(() => {
    const setOrientation = async () => {
      if (isConnected) {
        // Lock to landscape when connected
        await ScreenOrientation.lockAsync(
          ScreenOrientation.OrientationLock.LANDSCAPE
        );
      } else {
        // Unlock to portrait when disconnected
        await ScreenOrientation.lockAsync(
          ScreenOrientation.OrientationLock.PORTRAIT_UP
        );
      }
    };

    setOrientation();

    // Cleanup: unlock orientation on unmount
    return () => {
      ScreenOrientation.unlockAsync();
    };
  }, [isConnected]);

  // Start accelerometer sensor
  const startGyroscope = () => {
    // Set update interval to ~50ms (20 updates per second)
    Accelerometer.setUpdateInterval(50);

    gyroSubscription.current = Accelerometer.addListener((data) => {
      const newData = {
        x: parseFloat(data.x.toFixed(3)),
        y: parseFloat(data.y.toFixed(3)),
        z: parseFloat(data.z.toFixed(3)),
      };

      // Update both state and ref
      setGyroData(newData);
      gyroDataRef.current = newData;
    });
  };

  // Stop gyroscope sensor
  const stopGyroscope = () => {
    if (gyroSubscription.current) {
      gyroSubscription.current.remove();
      gyroSubscription.current = null;
    }
    if (sendIntervalRef.current) {
      clearInterval(sendIntervalRef.current);
      sendIntervalRef.current = null;
    }
  };

  // Send gyroscope data via WebSocket
  const sendGyroData = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Use ref to get the most current data
      const payload = JSON.stringify({
        x: gyroDataRef.current.x,
        y: gyroDataRef.current.y,
        z: gyroDataRef.current.z,
        gas: isGasPressedRef.current,
        brake: isBrakePressedRef.current,
      });
      wsRef.current.send(payload);
    }
  };

  // Connect to WebSocket server
  const connectWebSocket = () => {
    if (!serverUrl.trim()) {
      Alert.alert("Error", "Please enter a valid WebSocket server URL");
      return;
    }

    // Reset error flag when manually connecting
    hasShownErrorRef.current = false;
    reconnectAttemptRef.current = 0;

    try {
      setConnectionStatus("Connecting...");

      // Create WebSocket connection
      wsRef.current = new WebSocket(serverUrl);

      // Connection opened
      wsRef.current.onopen = () => {
        setConnectionStatus("Connected");
        setIsConnected(true);
        console.log("WebSocket connected");

        // Start gyroscope when connected
        startGyroscope();

        // Send gyroscope data every 50ms
        sendIntervalRef.current = setInterval(() => {
          sendGyroData(); // No parameter needed, uses ref internally
        }, 50);
      };

      // Listen for messages (optional)
      wsRef.current.onmessage = (event) => {
        console.log("Message from server:", event.data);
      };

      // Connection error
      wsRef.current.onerror = (error) => {
        console.error("WebSocket error:", error);
        setConnectionStatus("Connection Failed");

        // Show error alert only once
        if (!hasShownErrorRef.current) {
          hasShownErrorRef.current = true;
          Alert.alert(
            "Connection Failed",
            `Could not connect to server.\n\nMake sure:\n• Your PC is running the server\n• Both devices are on the same Wi-Fi\n• You're using the correct IP address\n\nYour phone IP: Check in terminal\nServer should show: "0.0.0.0:5000"`,
            [
              {
                text: "OK",
                onPress: () => {
                  hasShownErrorRef.current = false;
                },
              },
            ]
          );
        }
      };

      // Connection closed
      wsRef.current.onclose = (event) => {
        console.log("WebSocket closed:", event.code, event.reason);
        setConnectionStatus("Disconnected");
        setIsConnected(false);
        stopGyroscope();
        reconnectAttemptRef.current = 0;

        // NO auto-reconnect - user must manually reconnect
      };
    } catch (error) {
      console.error("Error creating WebSocket:", error);
      setConnectionStatus("Error");
      Alert.alert("Error", "Failed to create WebSocket connection");
    }
  };

  // Disconnect from WebSocket
  const disconnectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close(1000, "User disconnected"); // 1000 = normal closure
      wsRef.current = null;
    }
    stopGyroscope();
    setConnectionStatus("Disconnected");
    setIsConnected(false);
  };

  // Handle connect/disconnect button
  const handleConnectionToggle = () => {
    if (isConnected) {
      disconnectWebSocket();
    } else {
      connectWebSocket();
    }
  };

  // Get status color based on connection state
  const getStatusColor = () => {
    switch (connectionStatus) {
      case "Connected":
        return "#4CAF50";
      case "Connecting...":
        return "#FF9800";
      case "Error":
        return "#F44336";
      default:
        return "#9E9E9E";
    }
  };

  // Handle gas button press
  const handleGasPressIn = () => {
    setIsGasPressed(true);
    isGasPressedRef.current = true;
  };

  const handleGasPressOut = () => {
    setIsGasPressed(false);
    isGasPressedRef.current = false;
  };

  // Handle brake button press
  const handleBrakePressIn = () => {
    setIsBrakePressed(true);
    isBrakePressedRef.current = true;
  };

  const handleBrakePressOut = () => {
    setIsBrakePressed(false);
    isBrakePressedRef.current = false;
  };

  // Render Steering Screen (when connected)
  if (isConnected) {
    return (
      <SafeAreaView style={styles.steeringContainer}>
        <StatusBar hidden />

        {/* Disconnect button (top-center) */}
        <TouchableOpacity
          style={styles.disconnectBtn}
          onPress={disconnectWebSocket}
        >
          <Text style={styles.disconnectText}>✕ Disconnect</Text>
        </TouchableOpacity>

        {/* Main steering area */}
        <View style={styles.steeringArea}>
          {/* Brake Button (LEFT) */}
          <TouchableOpacity
            style={[
              styles.controlButton,
              styles.brakeButton,
              isBrakePressed && styles.buttonPressed,
            ]}
            onPressIn={handleBrakePressIn}
            onPressOut={handleBrakePressOut}
            activeOpacity={0.8}
          >
            <Text style={styles.buttonIcon}>🔻</Text>
            <Text style={styles.buttonLabel}>BRAKE</Text>
            <Text style={styles.buttonKey}>↓</Text>
          </TouchableOpacity>

          {/* Center Info */}
          <View style={styles.centerInfo}>
            <Text style={styles.steeringTitle}>🏎️ STEERING</Text>
            <Text style={styles.steeringValue}>
              {gyroData.y > 0.3
                ? "RIGHT ➡️"
                : gyroData.y < -0.3
                ? "LEFT ⬅️"
                : "CENTER"}
            </Text>
            <View style={styles.dataDisplay}>
              <Text style={styles.miniData}>Y: {gyroData.y.toFixed(2)}</Text>
            </View>
          </View>

          {/* Gas Button (RIGHT) */}
          <TouchableOpacity
            style={[
              styles.controlButton,
              styles.gasButton,
              isGasPressed && styles.buttonPressed,
            ]}
            onPressIn={handleGasPressIn}
            onPressOut={handleGasPressOut}
            activeOpacity={0.8}
          >
            <Text style={styles.buttonIcon}>🔺</Text>
            <Text style={styles.buttonLabel}>GAS</Text>
            <Text style={styles.buttonKey}>↑</Text>
          </TouchableOpacity>
        </View>

        {/* Bottom indicator */}
        <View style={styles.bottomIndicator}>
          <Text style={styles.indicatorText}>
            📡 Connected • Hold phone HORIZONTAL 🏎️
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  // Render Connection Screen (when not connected)
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={styles.content}>
        {/* Header */}
        <Text style={styles.title}>🎮 Steering Wheel Controller</Text>
        <Text style={styles.subtitle}>
          Hold phone horizontal like a steering wheel
        </Text>

        {/* Server URL Input */}
        <View style={styles.inputContainer}>
          <Text style={styles.label}>WebSocket Server URL:</Text>
          <TextInput
            style={styles.input}
            value={serverUrl}
            onChangeText={setServerUrl}
            placeholder="ws://192.168.1.42:5000"
            placeholderTextColor="#999"
            editable={!isConnected}
            autoCapitalize="none"
            autoCorrect={false}
          />
        </View>

        {/* Connection Status */}
        <View style={styles.statusContainer}>
          <View
            style={[styles.statusDot, { backgroundColor: getStatusColor() }]}
          />
          <Text style={styles.statusText}>{connectionStatus}</Text>
        </View>

        {/* Connect/Disconnect Button */}
        <TouchableOpacity
          style={[
            styles.button,
            isConnected ? styles.disconnectButton : styles.connectButton,
          ]}
          onPress={handleConnectionToggle}
        >
          <Text style={styles.buttonText}>
            {isConnected ? "Disconnect" : "Connect"}
          </Text>
        </TouchableOpacity>

        {/* Accelerometer Data Display */}
        <View style={styles.dataContainer}>
          <Text style={styles.dataTitle}>🏎️ Steering Wheel Mode</Text>

          <View style={styles.dataRow}>
            <Text style={styles.dataLabel}>X-Axis (Up/Down):</Text>
            <Text style={styles.dataValue}>{gyroData.x.toFixed(3)}</Text>
          </View>

          <View style={styles.dataRow}>
            <Text style={styles.dataLabel}>Y-Axis (STEERING):</Text>
            <Text style={[styles.dataValue, { color: "#FF9800" }]}>
              {gyroData.y.toFixed(3)}
            </Text>
          </View>

          <View style={styles.dataRow}>
            <Text style={styles.dataLabel}>Z-Axis (Gravity):</Text>
            <Text style={styles.dataValue}>{gyroData.z.toFixed(3)}</Text>
          </View>

          {isConnected && (
            <Text style={styles.transmissionNote}>
              📡 Sending data • 🏎️ Hold phone HORIZONTAL
            </Text>
          )}
        </View>

        {/* Info Box */}
        <View style={styles.infoBox}>
          <Text style={styles.infoTitle}>
            📡 How to Find Your PC's IP Address
          </Text>
          <Text style={styles.infoText}>
            1. On your PC, open PowerShell{"\n"}
            2. Type: ipconfig{"\n"}
            3. Look for "IPv4 Address" (e.g., 192.168.1.251){"\n"}
            4. Enter: ws://YOUR_IP:5000
          </Text>
          <Text style={[styles.infoText, { marginTop: 10, color: "#FF9800" }]}>
            ⚠️ Both devices must be on the same Wi-Fi network!
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#1a1a1a",
  },
  content: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#fff",
    textAlign: "center",
    marginTop: 20,
  },
  subtitle: {
    fontSize: 14,
    color: "#999",
    textAlign: "center",
    marginTop: 5,
    marginBottom: 30,
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    color: "#fff",
    marginBottom: 8,
    fontWeight: "600",
  },
  input: {
    backgroundColor: "#2a2a2a",
    borderRadius: 8,
    padding: 15,
    color: "#fff",
    fontSize: 16,
    borderWidth: 1,
    borderColor: "#444",
  },
  statusContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 20,
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  statusText: {
    fontSize: 16,
    color: "#fff",
    fontWeight: "600",
  },
  button: {
    padding: 16,
    borderRadius: 8,
    alignItems: "center",
    marginBottom: 30,
  },
  connectButton: {
    backgroundColor: "#2196F3",
  },
  disconnectButton: {
    backgroundColor: "#F44336",
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "bold",
  },
  dataContainer: {
    backgroundColor: "#2a2a2a",
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
  },
  dataTitle: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 15,
    textAlign: "center",
  },
  dataRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#444",
  },
  dataLabel: {
    fontSize: 16,
    color: "#999",
    fontWeight: "600",
  },
  dataValue: {
    fontSize: 20,
    color: "#4CAF50",
    fontWeight: "bold",
    fontFamily: "monospace",
  },
  transmissionNote: {
    fontSize: 12,
    color: "#FF9800",
    textAlign: "center",
    marginTop: 15,
    fontStyle: "italic",
  },
  infoBox: {
    backgroundColor: "#2a2a2a",
    borderRadius: 8,
    padding: 15,
    borderLeftWidth: 4,
    borderLeftColor: "#2196F3",
  },
  infoTitle: {
    fontSize: 14,
    color: "#fff",
    fontWeight: "600",
    marginBottom: 8,
  },
  infoText: {
    fontSize: 12,
    color: "#999",
    lineHeight: 18,
  },

  // Steering Screen Styles
  steeringContainer: {
    flex: 1,
    backgroundColor: "#000",
  },
  disconnectBtn: {
    position: "absolute",
    top: 20,
    left: "50%",
    transform: [{ translateX: -60 }],
    backgroundColor: "rgba(244, 67, 54, 0.8)",
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 25,
    zIndex: 10,
  },
  disconnectText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
  steeringArea: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
  },
  controlButton: {
    width: width * 0.25,
    height: height * 0.7,
    borderRadius: 20,
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  brakeButton: {
    backgroundColor: "#F44336",
  },
  gasButton: {
    backgroundColor: "#4CAF50",
  },
  buttonPressed: {
    opacity: 0.6,
    transform: [{ scale: 0.95 }],
  },
  buttonIcon: {
    fontSize: 48,
    marginBottom: 10,
  },
  buttonLabel: {
    color: "#fff",
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 5,
  },
  buttonKey: {
    color: "#fff",
    fontSize: 32,
    fontWeight: "bold",
    marginTop: 10,
  },
  centerInfo: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  steeringTitle: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 10,
  },
  steeringValue: {
    fontSize: 28,
    color: "#FF9800",
    fontWeight: "bold",
    marginBottom: 20,
  },
  dataDisplay: {
    backgroundColor: "rgba(255, 255, 255, 0.1)",
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 10,
  },
  miniData: {
    color: "#fff",
    fontSize: 18,
    fontFamily: "monospace",
  },
  bottomIndicator: {
    position: "absolute",
    bottom: 20,
    left: 0,
    right: 0,
    alignItems: "center",
  },
  indicatorText: {
    color: "#4CAF50",
    fontSize: 14,
    fontWeight: "600",
  },
});
