package servlets;

import java.io.IOException;
import java.io.StringReader;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import HTTPeXist.HTTPeXist;

public class ListResources extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private HTTPeXist eXist;

	public void init(ServletConfig config) {
		eXist = new HTTPeXist("http://localhost:8080");
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		String collection = request.getParameter("collection");
		if (collection == null) collection = "";

		String data = eXist.list(collection);
		Map<String, String> listaSVG = new HashMap<>();

		if (data == null || data.trim().isEmpty()) {
			request.setAttribute("informacion", "La colección '" + collection + "' no existe o está inaccesible.");
			request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
			return;
		}

		try {
			Document doc = convertStringToXMLDocument(data);
			// Buscamos los recursos dentro del XML devuelto por eXist
			NodeList valorNode = doc.getElementsByTagName("exist:resource");

			int numRecursos = valorNode.getLength();
			System.out.println("--> Recursos encontrados en " + collection + ": " + numRecursos);

			// Si no hay recursos, no entramos al bucle y evitamos el error
			for (int i = 0; i < numRecursos; i++) {
				String nombre = valorNode.item(i).getAttributes().getNamedItem("name").getNodeValue();
				String imagen = eXist.read(collection, nombre);
				listaSVG.put(nombre, imagen);
			}

			request.setAttribute("collection", collection);
			request.setAttribute("listaSVG", listaSVG);

			if (numRecursos == 0) {
				request.setAttribute("informacion", "La colección está vacía.");
			}

			RequestDispatcher rd = request.getRequestDispatcher("/jsp/imagenList.jsp");
			rd.forward(request, response);

		} catch (Exception e) {
			e.printStackTrace();
			request.setAttribute("informacion", "Error al procesar la lista de recursos: " + e.getMessage());
			request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
		}
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);
	}

	private static Document convertStringToXMLDocument(String xmlString) {
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		factory.setNamespaceAware(true);
		try {
			DocumentBuilder builder = factory.newDocumentBuilder();
			return builder.parse(new InputSource(new StringReader(xmlString)));
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
}