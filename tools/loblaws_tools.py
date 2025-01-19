def get_product_grid(pages):
    if not pages:
        return None

    layout = pages.get('layout')
    if not layout:
        return None

    sections = layout.get('sections')
    if not sections:
        return None

    product_listing_section = sections.get('productListingSection')
    if not product_listing_section:
        return None

    components = product_listing_section.get('components')
    if not components:
        return None

    data = components[0].get('data')
    if not data:
        return None

    product_grid = data.get('productGrid')
    if not product_grid:
        return None

    product_tiles = product_grid.get('productTiles')
    if not product_tiles:
        return None

    if product_tiles:
        return True