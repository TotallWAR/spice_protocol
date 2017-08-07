using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace ClientForWindows
{

    public class StateObject
    {
        public Socket workSocket = null;
        public const int BufferSize = 256;
        public byte[] buffer = new byte[BufferSize];
        public StringBuilder sb = new StringBuilder();
    }


    public class Client
    {

        Dictionary<int, string> errorsDictionary = new Dictionary<int, string>()
        {
            {400, "Некорректный запрос"},
            {401, "Ошибка авторизации"},
            {404, "Отсутствует виртуальная машина"}
        };


        private const int port = 23004;

        private static ManualResetEvent connectDone = new ManualResetEvent(false);
        private static ManualResetEvent sendDone = new ManualResetEvent(false);
        private static ManualResetEvent receiveDone = new ManualResetEvent(false);

        private static string resp = string.Empty;

        private static Exception check = null;
        public static Exception MakeConnection(string login, string password, out string responce)
        {
            try
            {
                 connectDone = new ManualResetEvent(false);
                sendDone = new ManualResetEvent(false);
                receiveDone = new ManualResetEvent(false);

        // адрес хоста
                IPHostEntry ipHostInfo = Dns.Resolve("10.11.1.75");
                IPAddress ipAddress = ipHostInfo.AddressList[0];

        
                IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);

                Socket client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

                client.BeginConnect(remoteEP, new AsyncCallback(ConnectCallback), client);

                if (check != null)
                {
                    responce = string.Empty;
                    client.Shutdown(SocketShutdown.Both);
                    client.Close();
                    return check;
                }

                connectDone.WaitOne();


                if (check != null)
                {
                    responce = string.Empty;
                    client.Shutdown(SocketShutdown.Both);
                    client.Close();
                    return check;
                }

                string request = string.Format("{0} {1}", login, password);
                Send(client, request);

                if (check != null)
                {
                    responce = string.Empty;
                    client.Shutdown(SocketShutdown.Both);
                    client.Close();
                    return check;
                }

                sendDone.WaitOne();

                if (check != null)
                {
                    responce = string.Empty;
                    client.Shutdown(SocketShutdown.Both);
                    client.Close();
                    return check;
                }

                Receive(client);

               


                receiveDone.WaitOne();

                if (check != null)
                {
                    responce = string.Empty;
                    client.Shutdown(SocketShutdown.Both);
                    client.Close();
                    return check;
                }


                client.Shutdown(SocketShutdown.Both);
                client.Close();

                responce = resp;
                return null;
                   
            }
            catch (Exception e)
            {
                responce = string.Empty;
                return e;
            }
        }

        private static void ConnectCallback(IAsyncResult ar)
        {
         try
         {
                Socket client = (Socket)ar.AsyncState;
                client.EndConnect(ar);
                connectDone.Set();
                
          } catch (Exception e) {
              check = e;
          }
           
        }


        private static void Send(Socket client, String data)
        {
            try
            {
                byte[] byteData = Encoding.ASCII.GetBytes(data);
                client.BeginSend(byteData, 0, byteData.Length, 0,
                    new AsyncCallback(SendCallback), client);
                
            }
            catch (Exception e)
            {
                check = e;
            }
        }

        private static void SendCallback(IAsyncResult ar)
        {
            try
            {
                Socket client = (Socket)ar.AsyncState;
                int bytesSent = client.EndSend(ar);
                sendDone.Set();
            }
            catch (Exception e)
            {
                check = e;
            }
        }


        private static void Receive(Socket client)
        {
            try
            {

                StateObject state = new StateObject();
                state.workSocket = client;
                client.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0,
                    new AsyncCallback(ReceiveCallback), state);
                check = null;
            }
            catch (Exception e)
            {
                check = e;
            }
        }

        private static void ReceiveCallback(IAsyncResult ar)    
        {
            try
            {
                StateObject state = (StateObject)ar.AsyncState;
                Socket client = state.workSocket;
                int bytesRead = client.EndReceive(ar);

                if (bytesRead > 0)
                {

                    state.sb.Append(Encoding.ASCII.GetString(state.buffer, 0, bytesRead));
                }
               
                if (state.sb.Length > 1)
                {
                    resp = state.sb.ToString();
                }
                receiveDone.Set();
                
            }
            catch (Exception e)
            {
                check = e;
            }
        }




    }
}
