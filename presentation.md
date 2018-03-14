Consulta com debug.
```
{
  allThemes {
    edges {
      node {
        id
        name
      }
    }
  }

  __debug {
    sql {
      rawSql
    }
  }
}
```

Paginação
```
{
  allThemes(first: 2) {
    edges {
      node {
        id
        name
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
  __debug {
    sql {
      rawSql
    }
  }
}
```