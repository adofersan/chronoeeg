# ChronoEEG Development Notes

## Version History

### v0.1.0 (2025-10-26)
- Initial release
- Core modules: io, preprocessing, quality, features, pipeline
- Docker support
- Test infrastructure
- Documentation

## Architecture Decisions

### Why src/ Layout?
- Modern Python packaging best practice
- Clear separation between source and tests
- Easier to manage imports
- Better for editable installs

### Why Frequency Modulated Möbius (FMM)?
- Advanced signal decomposition method
- Möbius transformations in complex plane
- Time-varying frequency modulation
- Better captures EEG oscillatory dynamics

### Modular Design
- Each module has single responsibility
- Easy to extend with new features
- Testable components
- Flexible configuration

## Future Enhancements

### High Priority
- [ ] Add EDF/BDF format support
- [ ] Implement streaming analysis
- [ ] Add more visualization tools
- [ ] GPU acceleration for FMM

### Medium Priority
- [ ] Pre-trained models
- [ ] Real-time quality monitoring
- [ ] Interactive dashboards
- [ ] Cloud deployment support

### Low Priority
- [ ] Mobile app integration
- [ ] WebAssembly port
- [ ] Integration with EEG hardware

## Known Issues

1. FMM computation can be slow for large datasets
   - Solution: Implement parallel processing
   
2. Memory usage for long recordings
   - Solution: Implement chunked processing

## Performance Notes

- Classical features: ~0.5s per 5-min epoch
- FMM features: ~2-3s per 5-min epoch (10 components)
- Quality assessment: ~0.3s per 5-min epoch

## Testing Strategy

- Unit tests for each module
- Integration tests for pipelines
- Regression tests for feature extraction
- Performance benchmarks
