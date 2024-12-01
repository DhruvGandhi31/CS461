import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class TodoListServer {
    public static void main(String[] args) {
        try {
            TodoListImplementation obj = new TodoListImplementation();

            Registry registry = LocateRegistry.createRegistry(2000);
            registry.rebind("TodoListService", obj);

            System.out.println("To-Do List Server is ready.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
