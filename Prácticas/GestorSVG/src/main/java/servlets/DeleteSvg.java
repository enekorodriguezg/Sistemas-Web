package servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import HTTPeXist.HTTPeXist;

public class DeleteSvg extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // 1. Capturar parámetros (vienen de los enlaces en imagenList.jsp)
        String collection = request.getParameter("collection");
        String svgName = request.getParameter("svgName");

        // Validación básica: si no hay datos, volvemos al inicio
        if (collection == null || svgName == null) {
            response.sendRedirect(request.getContextPath() + "/jsp/index.jsp");
            return;
        }

        try {
            // 2. Conectar con eXist y borrar
            HTTPeXist api = new HTTPeXist("http://localhost:8080");
            int status = api.delete(collection, svgName);

            // 3. Preparar mensaje de feedback
            if (status == 200 || status == 204) {
                request.setAttribute("informacion", "Imagen '" + svgName + "' eliminada correctamente.");
            } else {
                request.setAttribute("informacion", "Error al eliminar: el servidor devolvió " + status);
            }

        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("informacion", "Excepción al eliminar: " + e.getMessage());
        }

        // 4. Volvemos a la lista de la colección
        // Usamos un Forward al servlet ListResources (/apiLR) para que la lista se refresque
        request.getRequestDispatcher("/apiLR?collection=" + collection).forward(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }
}