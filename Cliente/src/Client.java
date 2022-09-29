import java.net.*;
import java.io.*;
import java.util.*;

import javax.swing.event.ListDataEvent;

public class Client {
    private Socket s;
    private DataInputStream in;
    private DataOutputStream out;
    private String topDeck;
    private List <String> hand;
    private List <String> deck;
    private List <String> pile1 = new ArrayList<String>();
    private List <String> pile2 = new ArrayList<String>();
    private List <String> pile3 = new ArrayList<String>();
    private List <String> pile4 = new ArrayList<String>();
    private String lastUsed = "";
    private String handSent = "";

    public Client(Socket s, DataInputStream in, DataOutputStream out, String[] deck){
        this.s = s;
        this.in = in;
        this.out = out;
        this.deck = new ArrayList<String>(Arrays.asList(deck));
        this.topDeck = deck[deck.length - 1];
    }

    public void seeCards(){
        System.out.println("Primera carta mi deck: " + topDeck);
        System.out.println("Cartas en mi deck: " + deck.size());

                    if(hand != null){
                        System.out.println("Mano: " + hand.toString());
                    }
                    else{
                        System.out.println("Mano: null");
                    }

                    if(pile1.size() >= 1){
                        System.out.println("Pila 1: " + pile1.get(pile1.size() - 1).toString() + " Cantidad Cartas en pila: " + pile1.size());
                    }
                    else{
                        System.out.println("Pila 1: null");
                    }

                    if(pile2.size() >= 1){
                        System.out.println("Pila 2: " + pile2.get(pile2.size() - 1).toString() + " Cantidad Cartas en pila: " + pile2.size());
                    }
                    else{
                        System.out.println("Pila 2: null");
                    }

                    if(pile3.size() >= 1){
                        System.out.println("Pila 3: " + pile3.get(pile3.size() - 1).toString() + " Cantidad Cartas en pila: " + pile3.size());
                    }
                    else{
                        System.out.println("Pila 3: null");
                    }

                    if(pile4.size() >= 1){
                        System.out.println("Pila 4: " + pile4.get(pile4.size() - 1).toString() + " Cantidad Cartas en pila: " + pile4.size());
                    }
                    else{
                        System.out.println("Pila 4: null");
                    }      
                    
    }

    public void sendMSG(){
        try{
            Scanner scan = new Scanner(System.in);

            while(s.isConnected()){
                String toSend = scan.nextLine();
                if(toSend.equals("/myCards")){

                    seeCards();
                    
                }
                else if(toSend.equals("/disconnect")){
                    out.writeUTF("/disconnect");
                    s.close();
                }
                else if(toSend.contains("/turn:toPile")){
                    try{
                        String[] parts = toSend.split(":");
                        if(parts[0].equals("/turn") && parts[1].equals("toPile")){
                            if(parts[2].contains("pile")){
                                String[] myPile = parts[2].split("-");
                                String[] serverPile = parts[3].split("-");

                                if(myPile[1].equals("1")){
                                    out.writeUTF("/turn:" + pile1.get(pile1.size() - 1).toString() + ":" + serverPile[1]);
                                    lastUsed = "pile1";
                                }
                                else if(myPile[1].equals("2")){
                                    out.writeUTF("/turn:" + pile2.get(pile2.size() - 1).toString() + ":" + serverPile[1]);
                                    lastUsed = "pile2";
                                }
                                else if(myPile[1].equals("3")){
                                    out.writeUTF("/turn:" + pile3.get(pile3.size() - 1).toString() + ":" + serverPile[1]);
                                    lastUsed = "pile3";
                                }
                                else if(myPile[1].equals("4")){
                                    out.writeUTF("/turn:" + pile4.get(pile4.size() - 1).toString() + ":" + serverPile[1]);
                                    lastUsed = "pile4";
                                }
                                else{
                                    System.out.println("Comando Invalido");
                                }
                            }
                            else if(parts[2].contains("hand")){
                                String[] myhand = parts[2].split("-");
                                String[] serverPile = parts[3].split("-");
                                if(hand.contains(myhand[1])){
                                    out.writeUTF("/turn:" + myhand[1] + ":" + serverPile[1]);
                                    lastUsed = "hand";
                                    handSent = myhand[1];
                                }
                                else{
                                    System.out.println("Comando Invalido");
                                }

                            }
                            else if(parts[2].contains("deck")){
                                String[] serverPile = parts[3].split("-");

                                if(deck.size() > 0){
                                    out.writeUTF("/turn:" + deck.get(deck.size() - 1).toString() + ":" + serverPile[1]);
                                    lastUsed = "deck";
                                }
                                else{
                                    System.out.println("Comando Invalido");
                                }

                            }
                            else{
                                System.out.println("Comando Invalido");
                            }
                        }


                    }catch(Exception e){
                        e.printStackTrace();
                        System.out.println("Comando Invalido");
                    }
                }
                else if(toSend.contains("/turn:discard")){
                    try{
                        String[] parts = toSend.split(":");
                        if(parts[0].equals("/turn") && parts[1].equals("discard")){
                            if(hand.contains(parts[2])){
                                if(parts[3].equals("1")){
                                    hand.remove(parts[2]);
                                    pile1.add(parts[2]);
                                    System.out.println("Carta Descartada");
                                    seeCards();
                                    out.writeUTF("/endTurn");
                                }
                                else if(parts[3].equals("2")){
                                    hand.remove(parts[2]);
                                    pile2.add(parts[2]);
                                    System.out.println("Carta Descartada");
                                    seeCards();
                                    out.writeUTF("/endTurn");
                                }
                                else if(parts[3].equals("3")){
                                    hand.remove(parts[2]);
                                    pile3.add(parts[2]);
                                    System.out.println("Carta Descartada");
                                    seeCards();
                                    out.writeUTF("/endTurn");
                                }
                                else if(parts[3].equals("4")){
                                    hand.remove(parts[2]);
                                    pile4.add(parts[2]);
                                    System.out.println("Carta Descartada");
                                    seeCards();
                                    out.writeUTF("/endTurn");
                                }
                            }
                        }
                    
                        else{
                            System.out.println("Comando Invalido");
                        }
                    }
                catch(Exception e){
                    e.printStackTrace();
                    System.out.println("Comando Invalido");
                }
            }

            else{
                out.writeUTF(toSend);
            }
                
        }
    }catch(Exception e){
        e.printStackTrace();
    }
}

    public void MSGlistener(){
        new Thread(new Runnable() {
            @Override
            public void run(){
                String recMSG;
                while(s.isConnected()){
                    try{
                        recMSG = in.readUTF();
                        if(recMSG.equals("/handSize")){
                            if(hand == null){
                                out.writeUTF("0");
                                recMSG = in.readUTF();
                                hand = new ArrayList<String>(Arrays.asList(recMSG.split(",")));
                                seeCards();
                            }
                            else{
                                out.writeUTF(Integer.toString(hand.size()));
                                recMSG = in.readUTF();
                                String[] add = recMSG.split(",");
                                for(int i = 0; i < add.length; i++){
                                    hand.add(add[i]);
                                }
                                seeCards();
                            }

                        }
                        else if(recMSG.equals("/removeLastTop")){
                            if(lastUsed.equals("pile1")){
                                pile1.remove(pile1.size() - 1);
                                lastUsed = "";
                            }
                            else if(lastUsed.equals("pile2")){
                                pile2.remove(pile2.size() - 1);
                                lastUsed = "";
                            }
                            else if(lastUsed.equals("pile3")){
                                pile3.remove(pile3.size() - 1);
                                lastUsed = "";
                            }
                            else if(lastUsed.equals("pile4")){
                                pile4.remove(pile4.size() - 1);
                                lastUsed = "";
                            }
                            else if(lastUsed.equals("hand")){
                                hand.remove(handSent);
                                lastUsed = "";
                                handSent = "";
                            }
                            else if(lastUsed.equals("deck")){
                                deck.remove(deck.size() - 1);
                                lastUsed = "";
                                topDeck = deck.get(deck.size() - 1);
                            }
                        }
                        else{
                            System.out.println(recMSG);
                        }
                        
                    }catch(Exception e){
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

}
