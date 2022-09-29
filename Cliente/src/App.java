
import java.net.*;
import java.io.*;
import java.util.Scanner;

public class App {

    public static void main(String[] args) throws Exception {


        Socket s = new Socket("localhost",8000);
        String msg;
        DataInputStream in = new DataInputStream(s.getInputStream());
        DataOutputStream out = new DataOutputStream(s.getOutputStream());
        Scanner scan = new Scanner(System.in);
        System.out.println("Ingrese su usuario: ");
        String user= scan.nextLine();
        out.writeUTF(user);
       
        /*msg = in.readUTF();
        System.out.println(msg);*/

        System.out.println("Ingrese su lobby: ");
        String lobby= scan.nextLine();
        out.writeUTF(lobby);
        String admin = "";
        while(s.isConnected()){
            if(admin.equals("")){
                System.out.println("Es admin? (y/n)");
                admin= scan.nextLine();
            }
            if(admin.equals("y")){
                System.out.println("Ingrese su accion:\n1)Iniciar el juego \n2)Permitir Ingreso \n3)Ver solicitudes de ingreso \n4)Desconectar");
                String mensaje= scan.nextLine();
                if(mensaje.equals("1")){
                    out.writeUTF("/startGame");
                    admin = "n";
                }
                else if(mensaje.equals("2")){
                    out.writeUTF("/approveRequest");
                    System.out.println("Ingrese el usuario: ");
                    String newMsg= scan.nextLine();
                    out.writeUTF(newMsg);

                    msg = in.readUTF();
                    System.out.println(msg);
                }
                else if(mensaje.equals("3")){
                    out.writeUTF("/viewRequests");
                }
                else if(mensaje.equals("4")){
                    out.writeUTF("/disconnect");
                    s.close();
                }
                else{
                    System.out.println("Comando Invalido");
                }
            }
            else if(admin.equals("n")){
                System.out.println("Espera a que inicie el juego");
                String deck;
                String deckArr[];
                deck = in.readUTF();
                deckArr = deck.split(",");
                Client cliente = new Client(s, in, out, deckArr);
                cliente.MSGlistener();
                cliente.sendMSG();
            }
            else{
                System.out.println("Invalido");
                admin = "";
            }       
        }
        s.close(); 

    }
}
