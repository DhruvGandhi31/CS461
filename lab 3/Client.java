import java.io.*;
import java.net.Socket;

public class Client {

    public static void main(String[] args) {
        // Replace with the Wi-Fi IP address of the server and respective port
        String SERVER_IP = "192.168.1.14"; // Same Wi-Fi IP address for all servers
        int SERVER_PORT = 5557; // Change this to connect to different servers (5555, 5556, etc.)

        try (Socket socket = new Socket(SERVER_IP, SERVER_PORT);
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in))) {

            // Start a thread to read server responses
            Thread readThread = new Thread(() -> {
                String response;
                try {
                    while ((response = in.readLine()) != null) {
                        System.out.println("Server: " + response);
                    }
                } catch (IOException e) {
                    System.err.println("Error reading from server: " + e.getMessage());
                }
            });
            readThread.start();

            // Sending user input to the server
            String message;
            while ((message = userInput.readLine()) != null) {
                out.println(message); // Send message to server
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
