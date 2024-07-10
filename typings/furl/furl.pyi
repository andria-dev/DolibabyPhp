"""
This type stub file was generated by pyright.
"""

import re
import abc
from furl.omdict1D import omdict1D
import six
from typing import Any, Dict, Iterable, List, Optional, Self
from .compat import UnicodeMixin

DEFAULT_PORTS = ...

def lget(lst, index, default=...) -> None: ...
def attemptstr(o) -> str: ...
def utf8(o, default=...) -> object: ...
def non_string_iterable(o) -> bool: ...
def idna_encode(o) -> str: ...
def idna_decode(o): ...
def is_valid_port(port) -> bool: ...
def static_vars(**kwargs) -> Callable[..., Any]: ...
def create_quote_fn(safe_charset, quote_plus) -> Callable[..., str]: ...

PERCENT_REGEX = ...
INVALID_HOST_CHARS = ...

@static_vars(
    regex=re.compile(
        r"^([\w%s]|(%s))*$" % (re.escape("-.~:@!$&'()*+,;="), PERCENT_REGEX)
    )
)
def is_valid_encoded_path_segment(segment) -> bool: ...
@static_vars(
    regex=re.compile(
        r"^([\w%s]|(%s))*$" % (re.escape("-.~:@!$&'()*+,;/?"), PERCENT_REGEX)
    )
)
def is_valid_encoded_query_key(key) -> bool: ...
@static_vars(
    regex=re.compile(
        r"^([\w%s]|(%s))*$" % (re.escape("-.~:@!$&'()*+,;/?="), PERCENT_REGEX)
    )
)
def is_valid_encoded_query_value(value) -> bool: ...
@static_vars(regex=re.compile(r"[a-zA-Z][a-zA-Z\-\.\+]*"))
def is_valid_scheme(scheme) -> bool: ...
@static_vars(regex=re.compile("[%s]" % re.escape(INVALID_HOST_CHARS)))
def is_valid_host(hostname) -> bool: ...
def get_scheme(url) -> Literal[""] | None: ...
def strip_scheme(url): ...
def set_scheme(url: str, scheme: Optional[str]) -> str: ...
def has_netloc(url): ...
def urlsplit(url) -> SplitResult:
    """
    Parameters:
      url: URL string to split.
    Returns: urlparse.SplitResult tuple subclass, just like
      urlparse.urlsplit() returns, with fields (scheme, netloc, path,
      query, fragment, username, password, hostname, port). See
        http://docs.python.org/library/urlparse.html#urlparse.urlsplit
      for more details on urlsplit().
    """
    ...

def urljoin(base: str, url: str) -> str:
    """
    Parameters:
      base: Base URL to join with <url>.
      url: Relative or absolute URL to join with <base>.

    Returns: The resultant URL from joining <base> and <url>.
    """
    ...

def join_path_segments(*args) -> list[Any]:
    """
    Join multiple lists of path segments together, intelligently
    handling path segments borders to preserve intended slashes of the
    final constructed path.

    This function is not encoding aware. It doesn't test for, or change,
    the encoding of path segments it is passed.

    Examples:
      join_path_segments(['a'], ['b']) == ['a','b']
      join_path_segments(['a',''], ['b']) == ['a','b']
      join_path_segments(['a'], ['','b']) == ['a','b']
      join_path_segments(['a',''], ['','b']) == ['a','','b']
      join_path_segments(['a','b'], ['c','d']) == ['a','b','c','d']

    Returns: A list containing the joined path segments.
    """
    ...

def remove_path_segments(segments, remove) -> list[Any]:
    """
    Removes the path segments of <remove> from the end of the path
    segments <segments>.

    Examples:
      # ('/a/b/c', 'b/c') -> '/a/'
      remove_path_segments(['','a','b','c'], ['b','c']) == ['','a','']
      # ('/a/b/c', '/b/c') -> '/a'
      remove_path_segments(['','a','b','c'], ['','b','c']) == ['','a']

    Returns: The list of all remaining path segments after the segments
    in <remove> have been removed from the end of <segments>. If no
    segments from <remove> were removed from <segments>, <segments> is
    returned unmodified.
    """
    ...

def quacks_like_a_path_with_segments(obj) -> bool: ...

class Path:
    """
    Represents a path comprised of zero or more path segments.

      http://tools.ietf.org/html/rfc3986#section-3.3

    Path parameters aren't supported.

    Attributes:
      _force_absolute: Function whos boolean return value specifies
        whether self.isabsolute should be forced to True or not. If
        _force_absolute(self) returns True, isabsolute is read only and
        raises an AttributeError if assigned to. If
        _force_absolute(self) returns False, isabsolute is mutable and
        can be set to True or False. URL paths use _force_absolute and
        return True if the netloc is non-empty (not equal to
        ''). Fragment paths are never read-only and their
        _force_absolute(self) always returns False.
      segments: List of zero or more path segments comprising this
        path. If the path string has a trailing '/', the last segment
        will be '' and self.isdir will be True and self.isfile will be
        False. An empty segment list represents an empty path, not '/'
        (though they have the same meaning).
      isabsolute: Boolean whether or not this is an absolute path or
        not. An absolute path starts with a '/'. self.isabsolute is
        False if the path is empty (self.segments == [] and str(path) ==
        '').
      strict: Boolean whether or not UserWarnings should be raised if
        improperly encoded path strings are provided to methods that
        take such strings, like load(), add(), set(), remove(), etc.
    """

    SAFE_SEGMENT_CHARS = ...
    def __init__(self, path=..., force_absolute=..., strict=...) -> None: ...
    def load(self, path) -> Self:
        """
        Load <path>, replacing any existing path. <path> can either be
        a Path instance, a list of segments, a path string to adopt.

        Returns: <self>.
        """
        ...

    def add(self, path) -> Self:
        """
        Add <path> to the existing path. <path> can either be a Path instance,
        a list of segments, or a path string to append to the existing path.

        Returns: <self>.
        """
        ...

    def set(self, path) -> Self: ...
    def remove(self, path) -> Self: ...
    def normalize(self) -> Self:
        """
        Normalize the path. Turn '//a/./b/../c//' into '/a/c/'.

        Returns: <self>.
        """
        ...

    def asdict(self) -> dict[str, str | Any | bool | list[str]]: ...
    @property
    def isabsolute(self) -> bool | list[str]: ...
    @isabsolute.setter
    def isabsolute(self, isabsolute) -> None:
        """
        Raises: AttributeError if _force_absolute(self) returns True.
        """
        ...

    @property
    def isdir(self) -> bool | list[str]:
        """
        Returns: True if the path ends on a directory, False
        otherwise. If True, the last segment is '', representing the
        trailing '/' of the path.
        """
        ...

    @property
    def isfile(self) -> bool:
        """
        Returns: True if the path ends on a file, False otherwise. If
        True, the last segment is not '', representing some file as the
        last segment of the path.
        """
        ...

    def __truediv__(self, path) -> Self: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    def __bool__(self) -> bool: ...

    __nonzero__ = ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

@six.add_metaclass(abc.ABCMeta)
class PathCompositionInterface:
    """
    Abstract class interface for a parent class that contains a Path.
    """
    def __init__(self, strict=...) -> None:
        """
        Params:
          force_absolute: See Path._force_absolute.

        Assignments to <self> in __init__() must be added to
        __setattr__() below.
        """
        ...

    @property
    def path(self) -> Path: ...
    @property
    def pathstr(self) -> str:
        """This method is deprecated. Use str(furl.path) instead."""
        ...

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        Returns: True if this attribute is handled and set here, False
        otherwise.
        """
        ...

@six.add_metaclass(abc.ABCMeta)
class URLPathCompositionInterface(PathCompositionInterface):
    """
    Abstract class interface for a parent class that contains a URL
    Path.

    A URL path's isabsolute attribute is absolute and read-only if a
    netloc is defined. A path cannot start without '/' if there's a
    netloc. For example, the URL 'http://google.coma/path' makes no
    sense. It should be 'http://google.com/a/path'.

    A URL path's isabsolute attribute is mutable if there's no
    netloc. The scheme doesn't matter. For example, the isabsolute
    attribute of the URL path in 'mailto:user@host.com', with scheme
    'mailto' and path 'user@host.com', is mutable because there is no
    netloc. See

      http://en.wikipedia.org/wiki/URI_scheme#Examples
    """
    def __init__(self, strict=...) -> None: ...

@six.add_metaclass(abc.ABCMeta)
class FragmentPathCompositionInterface(PathCompositionInterface):
    """
    Abstract class interface for a parent class that contains a Fragment
    Path.

    Fragment Paths they be set to absolute (self.isabsolute = True) or
    not absolute (self.isabsolute = False).
    """
    def __init__(self, strict=...) -> None: ...

class Query:
    """
    Represents a URL query comprised of zero or more unique parameters
    and their respective values.

      http://tools.ietf.org/html/rfc3986#section-3.4


    All interaction with Query.params is done with unquoted strings. So

      f.query.params['a'] = 'a%5E'

    means the intended value for 'a' is 'a%5E', not 'a^'.


    Query.params is implemented as an omdict1D object - a one
    dimensional ordered multivalue dictionary. This provides support for
    repeated URL parameters, like 'a=1&a=2'. omdict1D is a subclass of
    omdict, an ordered multivalue dictionary. Documentation for omdict
    can be found here

      https://github.com/gruns/orderedmultidict

    The one dimensional aspect of omdict1D means that a list of values
    is interpreted as multiple values, not a single value which is
    itself a list of values. This is a reasonable distinction to make
    because URL query parameters are one dimensional: query parameter
    values cannot themselves be composed of sub-values.

    So what does this mean? This means we can safely interpret

      f = furl('http://www.google.com')
      f.query.params['arg'] = ['one', 'two', 'three']

    as three different values for 'arg': 'one', 'two', and 'three',
    instead of a single value which is itself some serialization of the
    python list ['one', 'two', 'three']. Thus, the result of the above
    will be

      f.query.allitems() == [
        ('arg','one'), ('arg','two'), ('arg','three')]

    and not

      f.query.allitems() == [('arg', ['one', 'two', 'three'])]

    The latter doesn't make sense because query parameter values cannot
    be composed of sub-values. So finally

      str(f.query) == 'arg=one&arg=two&arg=three'


    Additionally, while the set of allowed characters in URL queries is
    defined in RFC 3986 section 3.4, the format for encoding key=value
    pairs within the query is not. In turn, the parsing of encoded
    key=value query pairs differs between implementations.

    As a compromise to support equal signs in both key=value pair
    encoded queries, like

      https://www.google.com?a=1&b=2

    and non-key=value pair encoded queries, like

      https://www.google.com?===3===

    equal signs are percent encoded in key=value pairs where the key is
    non-empty, e.g.

      https://www.google.com?equal-sign=%3D

    but not encoded in key=value pairs where the key is empty, e.g.

      https://www.google.com?===equal=sign===

    This presents a reasonable compromise to accurately reproduce
    non-key=value queries with equal signs while also still percent
    encoding equal signs in key=value pair encoded queries, as
    expected. See

      https://github.com/gruns/furl/issues/99

    for more details.

    Attributes:
      params: Ordered multivalue dictionary of query parameter key:value
        pairs. Parameters in self.params are maintained URL decoded,
        e.g. 'a b' not 'a+b'.
      strict: Boolean whether or not UserWarnings should be raised if
        improperly encoded query strings are provided to methods that
        take such strings, like load(), add(), set(), remove(), etc.
    """

    SAFE_KEY_CHARS = ...
    SAFE_VALUE_CHARS = ...
    def __init__(self, query=..., strict=...) -> None: ...
    def load(self, query) -> Self: ...
    def add(self, args) -> Self: ...
    def set(self, mapping) -> Self:
        """
        Adopt all mappings in <mapping>, replacing any existing mappings
        with the same key. If a key has multiple values in <mapping>,
        they are all adopted.

        Examples:
          Query({1:1}).set([(1,None),(2,2)]).params.allitems()
            == [(1,None),(2,2)]
          Query({1:None,2:None}).set([(1,1),(2,2),(1,11)]).params.allitems()
            == [(1,1),(2,2),(1,11)]
          Query({1:None}).set([(1,[1,11,111])]).params.allitems()
            == [(1,1),(1,11),(1,111)]

        Returns: <self>.
        """
        ...

    def remove(self, query) -> Self: ...
    @property
    def params(self) -> omdict1D: ...
    @params.setter
    def params(self, params) -> None: ...
    def encode(
        self, delimiter=..., quote_plus=..., dont_quote=..., delimeter=...
    ) -> str:
        """
        Examples:

          Query('a=a&b=#').encode() == 'a=a&b=%23'
          Query('a=a&b=#').encode(';') == 'a=a;b=%23'
          Query('a+b=c@d').encode(dont_quote='@') == 'a+b=c@d'
          Query('a+b=c@d').encode(quote_plus=False) == 'a%20b=c%40d'

        Until furl v0.4.6, the 'delimiter' argument was incorrectly
        spelled 'delimeter'. For backwards compatibility, accept both
        the correct 'delimiter' and the old, misspelled 'delimeter'.

        Keys and values are encoded application/x-www-form-urlencoded if
        <quote_plus> is True, percent-encoded otherwise.

        <dont_quote> exempts valid query characters from being
        percent-encoded, either in their entirety with dont_quote=True,
        or selectively with dont_quote=<string>, like
        dont_quote='/?@_'. Invalid query characters -- those not in
        self.SAFE_KEY_CHARS, like '#' and '^' -- are always encoded,
        even if included in <dont_quote>. For example:

          Query('#=^').encode(dont_quote='#^') == '%23=%5E'.

        Returns: A URL encoded query string using <delimiter> as the
        delimiter separating key:value pairs. The most common and
        default delimiter is '&', but ';' can also be specified. ';' is
        W3C recommended.
        """
        ...

    def asdict(self) -> dict[str, str | list[tuple[Any, Any]]]: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    def __bool__(self) -> bool: ...

    __nonzero__ = ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

@six.add_metaclass(abc.ABCMeta)
class QueryCompositionInterface:
    """
    Abstract class interface for a parent class that contains a Query.
    """
    def __init__(self, strict=...) -> None: ...
    @property
    def query(self) -> Query: ...
    @property
    def querystr(self) -> str:
        """This method is deprecated. Use str(furl.query) instead."""
        ...

    @property
    def args(self) -> omdict1D:
        """
        Shortcut method to access the query parameters, self._query.params.
        """
        ...

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        Returns: True if this attribute is handled and set here, False
        otherwise.
        """
        ...

class Fragment(FragmentPathCompositionInterface, QueryCompositionInterface):
    """
    Represents a URL fragment, comprised internally of a Path and Query
    optionally separated by a '?' character.

      http://tools.ietf.org/html/rfc3986#section-3.5

    Attributes:
      path: Path object from FragmentPathCompositionInterface.
      query: Query object from QueryCompositionInterface.
      separator: Boolean whether or not a '?' separator should be
        included in the string representation of this fragment. When
        False, a '?' character will not separate the fragment path from
        the fragment query in the fragment string. This is useful to
        build fragments like '#!arg1=val1&arg2=val2', where no
        separating '?' is desired.
    """
    def __init__(self, fragment=..., strict=...) -> None: ...
    def load(self, fragment) -> None: ...
    def add(self, path=..., args=...) -> Self: ...
    def set(self, path=..., args=..., separator=...) -> Self: ...
    def remove(self, fragment=..., path=..., args=...) -> Self: ...
    def asdict(
        self,
    ) -> dict[
        str,
        str
        | bool
        | dict[str, str | Any | bool | list[str]]
        | dict[str, str | list[tuple[Any, Any]]],
    ]: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __setattr__(self, attr: str, value: Any) -> None: ...
    def __bool__(self) -> bool: ...

    __nonzero__ = ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

@six.add_metaclass(abc.ABCMeta)
class FragmentCompositionInterface:
    """
    Abstract class interface for a parent class that contains a
    Fragment.
    """
    def __init__(self, strict: bool = ...) -> None: ...
    @property
    def fragment(self) -> Fragment: ...
    @property
    def fragmentstr(self) -> str:
        """This method is deprecated. Use str(furl.fragment) instead."""
        ...

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        Returns: True if this attribute is handled and set here, False
        otherwise.
        """
        ...

class furl(
    URLPathCompositionInterface,
    QueryCompositionInterface,
    FragmentCompositionInterface,
    UnicodeMixin,
):
    """
    Object for simple parsing and manipulation of a URL and its
    components.

      scheme://username:password@host:port/path?query#fragment

    Attributes:
      strict: Boolean whether or not UserWarnings should be raised if
        improperly encoded path, query, or fragment strings are provided
        to methods that take such strings, like load(), add(), set(),
        remove(), etc.
      username: Username string for authentication. Initially None.
      password: Password string for authentication with
        <username>. Initially None.
      scheme: URL scheme. A string ('http', 'https', '', etc) or None.
        All lowercase. Initially None.
      host: URL host (hostname, IPv4 address, or IPv6 address), not
        including port. All lowercase. Initially None.
      port: Port. Valid port values are 1-65535, or None meaning no port
        specified.
      netloc: Network location. Combined host and port string. Initially
      None.
      path: Path object from URLPathCompositionInterface.
      query: Query object from QueryCompositionInterface.
      fragment: Fragment object from FragmentCompositionInterface.
    """
    def __init__(
        self,
        url: str = ...,
        args: Dict[str, str] | None = ...,
        path: List[str] | None = ...,
        fragment: str | None = ...,
        scheme: str | None = ...,
        netloc: str | None = ...,
        origin: str | None = ...,
        fragment_path: List[str] | None = ...,
        fragment_args: Dict[str, str] | None = ...,
        fragment_separator: bool = ...,
        host: str | None = ...,
        port: int | None = ...,
        query: str | None = ...,
        query_params: Dict[str, str] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        strict: bool = ...,
    ) -> None:
        """
        Raises: ValueError on invalid URL or invalid URL component(s) provided.
        """
        ...

    def load(self, url: str) -> Self:
        """
        Parse and load a URL.

        Raises: ValueError on invalid URL, like a malformed IPv6 address
        or invalid port.
        """
        ...

    @property
    def scheme(self) -> str | None: ...
    @scheme.setter
    def scheme(self, scheme: str | None) -> None: ...
    @property
    def host(self) -> str | None: ...
    @host.setter
    def host(self, host: str | None) -> None:
        """
        Raises: ValueError on invalid host or malformed IPv6 address.
        """
        ...

    @property
    def port(self) -> int | None: ...
    @port.setter
    def port(self, port: int | None) -> None:
        """
        The port value can be 1-65535 or None, meaning no port specified. If
        <port> is None and self.scheme is a known scheme in DEFAULT_PORTS,
        the default port value from DEFAULT_PORTS will be used.

        Raises: ValueError on invalid port.
        """
        ...

    @property
    def netloc(self) -> str | None: ...
    @netloc.setter
    def netloc(self, netloc: str | None) -> None:
        """
        Params:
          netloc: Network location string, like 'google.com' or
            'user:pass@google.com:99'.
        Raises: ValueError on invalid port or malformed IPv6 address.
        """
        ...

    @property
    def origin(self) -> str: ...
    @origin.setter
    def origin(self, origin: str) -> None: ...
    @property
    def url(self) -> str: ...
    @url.setter
    def url(self, url: str) -> Self: ...
    def add(
        self,
        args: Dict[str, str] = ...,
        path: List[str] = ...,
        fragment_path: List[str] = ...,
        fragment_args: Dict[str, str] = ...,
        query_params: Dict[str, str] = ...,
    ) -> Self:
        """
        Add components to a URL and return this furl instance, <self>.

        If both <args> and <query_params> are provided, a UserWarning is
        raised because <args> is provided as a shortcut for
        <query_params>, not to be used simultaneously with
        <query_params>. Nonetheless, providing both <args> and
        <query_params> behaves as expected, with query keys and values
        from both <args> and <query_params> added to the query - <args>
        first, then <query_params>.

        Parameters:
          args: Shortcut for <query_params>.
          path: A list of path segments to add to the existing path
            segments, or a path string to join with the existing path
            string.
          query_params: A dictionary of query keys and values or list of
            key:value items to add to the query.
          fragment_path: A list of path segments to add to the existing
            fragment path segments, or a path string to join with the
            existing fragment path string.
          fragment_args: A dictionary of query keys and values or list
            of key:value items to add to the fragment's query.

        Returns: <self>.

        Raises: UserWarning if redundant and possibly conflicting <args> and
        <query_params> were provided.
        """
        ...

    def set(
        self,
        args: Dict[str, str] = ...,
        path: List[str] = ...,
        fragment: str = ...,
        query: str = ...,
        scheme: str = ...,
        username: str = ...,
        password: str = ...,
        host: str = ...,
        port: int = ...,
        netloc: str = ...,
        origin: str = ...,
        query_params: Dict[str, str] = ...,
        fragment_path: List[str] = ...,
        fragment_args: Dict[str, str] = ...,
        fragment_separator: bool = ...,
    ) -> Self:
        """
        Set components of a url and return this furl instance, <self>.

        If any overlapping, and hence possibly conflicting, parameters
        are provided, appropriate UserWarning's will be raised. The
        groups of parameters that could potentially overlap are

          <scheme> and <origin>
          <origin>, <netloc>, and/or (<host> or <port>)
          <fragment> and (<fragment_path> and/or <fragment_args>)
          any two or all of <query>, <args>, and/or <query_params>

        In all of the above groups, the latter parameter(s) take
        precedence over the earlier parameter(s). So, for example

          furl('http://google.com/').set(
            netloc='yahoo.com:99', host='bing.com', port=40)

        will result in a UserWarning being raised and the url becoming

          'http://bing.com:40/'

        not

          'http://yahoo.com:99/

        Parameters:
          args: Shortcut for <query_params>.
          path: A list of path segments or a path string to adopt.
          fragment: Fragment string to adopt.
          scheme: Scheme string to adopt.
          netloc: Network location string to adopt.
          origin: Scheme and netloc.
          query: Query string to adopt.
          query_params: A dictionary of query keys and values or list of
            key:value items to adopt.
          fragment_path: A list of path segments to adopt for the
            fragment's path or a path string to adopt as the fragment's
            path.
          fragment_args: A dictionary of query keys and values or list
            of key:value items for the fragment's query to adopt.
          fragment_separator: Boolean whether or not there should be a
            '?' separator between the fragment path and fragment query.
          host: Host string to adopt.
          port: Port number to adopt.
          username: Username string to adopt.
          password: Password string to adopt.
        Raises:
          ValueError on invalid port.
          UserWarning if <scheme> and <origin> are provided.
          UserWarning if <origin>, <netloc> and/or (<host> and/or <port>) are
            provided.
          UserWarning if <query>, <args>, and/or <query_params> are provided.
          UserWarning if <fragment> and (<fragment_path>,
            <fragment_args>, and/or <fragment_separator>) are provided.
        Returns: <self>.
        """
        ...

    def remove(
        self,
        args: List[str] = ...,
        path: List[str] | str | bool = ...,
        fragment: bool = ...,
        query: List[str] | bool = ...,
        scheme: bool = ...,
        username: bool = ...,
        password: bool = ...,
        host: bool = ...,
        port: bool = ...,
        netloc: bool = ...,
        origin: bool = ...,
        query_params: List[str] = ...,
        fragment_path: List[str] | str = ...,
        fragment_args: List[str] = ...,
    ) -> Self:
        """
        Remove components of this furl's URL and return this furl
        instance, <self>.

        Parameters:
          args: Shortcut for query_params.
          path: A list of path segments to remove from the end of the
            existing path segments list, or a path string to remove from
            the end of the existing path string, or True to remove the
            path portion of the URL entirely.
          query: A list of query keys to remove from the query, if they
            exist, or True to remove the query portion of the URL
            entirely.
          query_params: A list of query keys to remove from the query,
            if they exist.
          port: If True, remove the port from the network location
            string, if it exists.
          fragment: If True, remove the fragment portion of the URL
            entirely.
          fragment_path: A list of path segments to remove from the end
            of the fragment's path segments or a path string to remove
            from the end of the fragment's path string.
          fragment_args: A list of query keys to remove from the
            fragment's query, if they exist.
          username: If True, remove the username, if it exists.
          password: If True, remove the password, if it exists.
        Returns: <self>.
        """
        ...

    def tostr(
        self,
        query_delimiter: str = ...,
        query_quote_plus: bool = ...,
        query_dont_quote: str = ...,
    ) -> str: ...
    def join(self, *urls: Iterable[str]) -> Self: ...
    def copy(self) -> Self: ...
    def asdict(
        self,
    ) -> dict[
        str,
        str
        | Any
        | object
        | int
        | dict[str, str | Any | bool | list[str]]
        | dict[str, str | list[tuple[Any, Any]]]
        | dict[
            str,
            str
            | bool
            | dict[str, str | Any | bool | list[str]]
            | dict[str, str | list[tuple[Any, Any]]],
        ]
        | None,
    ]: ...
    def __truediv__(self, path: str) -> Self: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __setattr__(self, attr: str, value: Any) -> None: ...
    def __unicode__(self) -> str: ...
    def __repr__(self) -> str: ...
