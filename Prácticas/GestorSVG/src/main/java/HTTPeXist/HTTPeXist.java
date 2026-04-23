package HTTPeXist;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;

import org.exist.xmldb.XmldbURI;
import org.xml.sax.SAXException;

public class HTTPeXist {

	private String server;

	public HTTPeXist(String server) {
		super();
		this.server = server;
	}

	// El escudo contra el error "Illegal character in URL"
	private String encode(String pathSegment) throws UnsupportedEncodingException {
		if (pathSegment == null) return "";
		return URLEncoder.encode(pathSegment, "UTF-8").replace("+", "%20");
	}

	/* -->READ lee un recurso de una coleccion */
	public String read(String collection, String resourceName) throws IOException {
		String resource = "";
		// Aplicamos encode a cada segmento de la ruta
		URL url = new URL(this.server + "/exist/rest" + XmldbURI.ROOT_COLLECTION_URI + "/" + encode(collection) + "/" + encode(resourceName));
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("GET");

		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);

		InputStream connectInputStream = connect.getInputStream();
		BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(connectInputStream));
		String line;
		while ((line = bufferedReader.readLine()) != null) {
			resource = resource + line + "\n";
		}
		return resource;
	}

	/* -->LIST lista los recursos en una coleccion */
	public String list(String collection) throws IOException {
		String lista = "";
		URL url = new URL(this.server + "/exist/rest" + XmldbURI.ROOT_COLLECTION_URI + "/" + encode(collection));
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("GET");

		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);

		InputStream connectInputStream = connect.getInputStream();
		BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(connectInputStream));
		String line;
		while ((line = bufferedReader.readLine()) != null) {
			lista = lista + line + "\n";
		}
		return lista;
	}

	/* -->SUBIR recurso en un fichero */
	public int subir(String collection, String resourceFileName) throws IOException {
		File file = new File(resourceFileName);
		if (!file.canRead()) return -1;

		String document = file.getName();
		URL url = new URL(this.server + "/exist/rest" + XmldbURI.ROOT_COLLECTION_URI + "/" + encode(collection) + "/" + encode(document));
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("PUT");
		connect.setDoOutput(true);

		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);
		// CORREGIDO: Content-Type (con guion)
		connect.setRequestProperty("Content-Type", "application/xml");

		StringBuilder postData = new StringBuilder();
		try (BufferedReader bufferReader = new BufferedReader(new FileReader(file))) {
			String cadena;
			while ((cadena = bufferReader.readLine()) != null) {
				postData.append(cadena).append("\n");
			}
		}
		byte[] postDataBytes = postData.toString().getBytes("UTF-8");
		connect.setRequestProperty("Content-Length", String.valueOf(postDataBytes.length));
		connect.getOutputStream().write(postDataBytes);

		return connect.getResponseCode();
	}

	/* -->DELETE borrar un recurso */
	public int delete(String collection, String resourceName) throws IOException {
		URL url = new URL(this.server + "/exist/rest" + XmldbURI.ROOT_COLLECTION_URI + "/" + encode(collection) + "/" + encode(resourceName));
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("DELETE");
		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);
		return connect.getResponseCode();
	}

	/*-->SUBIR recurso en un String */
	public int subirString(String collection, String resource, String resourceName) throws IOException {
		URL url = new URL(this.server + "/exist/rest" + XmldbURI.ROOT_COLLECTION_URI + "/" + encode(collection) + "/" + encode(resourceName));
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("PUT");
		connect.setDoOutput(true);

		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);
		connect.setRequestProperty("Content-Type", "application/xml");

		byte[] postDataBytes = resource.getBytes("UTF-8");
		connect.setRequestProperty("Content-Length", String.valueOf(postDataBytes.length));
		connect.getOutputStream().write(postDataBytes);

		return connect.getResponseCode();
	}

	/* -->DELETE borrar coleccion */
	public int delete(String collection) throws IOException {
		URL url = new URL(this.server + "/exist/rest" + XmldbURI.ROOT_COLLECTION_URI + "/" + encode(collection));
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("DELETE");

		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);

		return connect.getResponseCode();
	}

	/*-->CORREGIDO: CREATE ahora crea una colección real usando XQuery */
	public int create(String collection) throws IOException {
		// Para crear una carpeta (colección), usamos la función de administración de eXist
		String query = "xmldb:create-collection('/db', '" + collection + "')";
		String urlStr = this.server + "/exist/rest/db?_query=" + codificaQuery(query);

		URL url = new URL(urlStr);
		HttpURLConnection connect = (HttpURLConnection) url.openConnection();
		connect.setRequestMethod("GET");

		String codigoBase64 = getAuthorizationCode("admin", "eneko200505");
		connect.setRequestProperty("Authorization", "Basic " + codigoBase64);

		int status = connect.getResponseCode();
		System.out.println("CREAR COLECCIÓN '" + collection + "' - Status: " + status);
		return status;
	}

	public static String getAuthorizationCode(String user, String pwd) {
		String codigo = user + ":" + pwd;
		return cifrarBase64(codigo);
	}

	public static String cifrarBase64(String a) {
		return Base64.getEncoder().encodeToString(a.getBytes(StandardCharsets.UTF_8));
	}

	public String codificaQuery(String query) {
		return query.replaceAll(" ", "%20").replaceAll("\\<", "%3C").replaceAll("\\>", "%3E").replaceAll("\\!", "%21")
				.replaceAll("\\#", "%23").replaceAll("\\$", "%24").replaceAll("\\'", "%27").replaceAll("\\(", "%28")
				.replaceAll("\\)", "%29").replaceAll("\\*", "%2A").replaceAll("\\+", "%2B").replaceAll("\\,", "%2C")
				.replaceAll("\\:", "%3A").replaceAll("\\;", "%3B").replaceAll("\\=", "%3D").replaceAll("\\?", "%3F")
				.replaceAll("\\@", "%40").replaceAll("\\[", "%5B").replaceAll("\\]", "%5D");
	}

	public static void main(String[] args) throws Exception {
		HTTPeXist prueba = new HTTPeXist("http://localhost:8080");
		prueba.read("SVG_imagenes", "camion.svg");
	}
}