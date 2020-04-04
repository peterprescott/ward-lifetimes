FROM darribas/gds_py:4.0

RUN conda install pyreadstat -y \
    && conda install geoplot -y \
    && conda install mlxtend --channel conda-forge -y
    
CMD bash
