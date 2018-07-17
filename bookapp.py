import re
import traceback

from bookdb import BookDB

DB = BookDB()


def book(book_id):

    body = "<p>"
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    for field, data in book.items():
        body += "<b>{}:</b> {}<br>".format(field, data)
    body += "</p>"
    return body


def books():
    body = '<h1>My bookshelf:</h1>\r\n<ul>'

    for book in DB.titles():
        body += '<li><a href="/book/' + book['id'] + '">' + book['title'] + '</a></li>\r\n'
    body += '</ul>'
    return body

def resolve_path(path):
    funcs = {
        '': books,
        'book': book,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
