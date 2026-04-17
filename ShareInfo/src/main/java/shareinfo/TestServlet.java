package shareinfo;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

import helper.db.*;

public class TestServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private MySQLdb mySQLdb;

    public TestServlet(){
        super();
        mySQLdb=new MySQLdb();
    }
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        System.out.println("‐‐‐> doPost() de TestServlet");
        PrintWriter http_out=response.getWriter();
        String type = request.getParameter("type");
        if (type != null ) {
            if (type.equals("registerUser")) {
                System.out.println("‐‐‐‐ Solicitado registrar un usuario");
                String email = request.getParameter("email");
                String password = request.getParameter("password");
                String username = request.getParameter("username");
                if (email != null && password != null && username != null ) {
                    System.out.println("‐‐‐‐ Parametros: "+ email + " ‐ " + password + " ‐ " + username );
                    mySQLdb.setUserInfo(email, password, username);
                    http_out.println("El almacenamiento se ha realizado correctamente");
                }
                else { http_out.println("No se han enviado bien los parámetro");
                }
            }
        } else {
            http_out.println("No se ha enviado el parámetro type");
        }
        System.out.println("<‐‐‐ doPost() de TestServlet");
    }
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }
}

