import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.List;

public class TodoListImplementation extends UnicastRemoteObject implements TodoListInterface {
    private List<String> tasks;

    protected TodoListImplementation() throws RemoteException {
        super();
        tasks = new ArrayList<>();
    }

    @Override
    public void addTask(String task) throws RemoteException {
        tasks.add(task);
    }

    @Override
    public void removeTask(String task) throws RemoteException {
        tasks.remove(task);
    }

    @Override
    public List<String> listTasks() throws RemoteException {
        return tasks;
    }
}
