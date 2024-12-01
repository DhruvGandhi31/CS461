import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.List;
import java.util.Scanner;

public class TodoListClient {
    public static void main(String[] args) {
        try {
            // Locate the registry
            Registry registry = LocateRegistry.getRegistry("localhost", 2000);

            // Look up the remote object
            TodoListInterface stub = (TodoListInterface) registry.lookup("TodoListService");
            Scanner scanner = new Scanner(System.in);
            String command;

            System.out.println("Welcome to the To-Do List application!");
            do {
                System.out.println("Enter a command (add, remove, list, exit):");
                command = scanner.nextLine();

                switch (command.toLowerCase()) {
                    case "add":
                        System.out.println("Enter task to add:");
                        String taskToAdd = scanner.nextLine();
                        stub.addTask(taskToAdd);
                        System.out.println("Task added.");
                        break;
                    case "remove":
                        System.out.println("Enter task to remove:");
                        String taskToRemove = scanner.nextLine();
                        stub.removeTask(taskToRemove);
                        System.out.println("Task removed.");
                        break;
                    case "list":
                        List<String> tasks = stub.listTasks();
                        System.out.println("Current tasks:");
                        for (String task : tasks) {
                            System.out.println("- " + task);
                        }
                        break;
                    case "exit":
                        System.out.println("Exiting application.");
                        break;
                    default:
                        System.out.println("Invalid command. Try again.");
                }
            } while (!command.equalsIgnoreCase("exit"));

            scanner.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
