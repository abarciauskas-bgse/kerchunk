
import fsspec


def single_zarr(uri_or_store, storage_options=None):
    """kerchunk-style view on zarr mapper

    This is a similar process to zarr's consolidate_metadata, but does not
    need to be held in the original file tree. You do not need zarr itself
    to do this.

    This is useful for testing, so that we can pass hand-made zarrs to combine.
    """

    # TODO: support a zarr group or FSStore?
    if isinstance(uri_or_store, str):
        mapper = fsspec.get_mapper(uri_or_store, **(storage_options or {}))
    else:
        mapper = uri_or_store

    refs = {}
    for k in mapper:
        if k.startswith("."):
            refs[k] = mapper[k]
        else:
            refs[k] = [fsspec.utils._unstrip_protocol(mapper._key_to_str(k), mapper.fs)]
    return refs
